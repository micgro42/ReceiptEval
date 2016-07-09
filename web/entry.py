# -*- coding: utf-8 -*-

from colander import MappingSchema
from colander import SequenceSchema
from colander import SchemaNode
from colander import String
from colander import Date
from colander import Decimal
from colander import Integer
import colander

from deform import ValidationFailure
from deform import Form
from deform import widget


import peppercorn
import itertools

from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from receipteval.storage.sqlite import sqlite

import json
import pprint
from collections import defaultdict

counter = itertools.count()

class ItemSchema(MappingSchema):
    db = sqlite()
    name  = SchemaNode(String(),
                        description = 'Bezeichnung des Items',
                        title='Name')
    categories = db.getAllCategories()
    categories = [(cat, cat) for (cat, comment) in categories]
    category = SchemaNode(
                String(),
                widget=widget.SelectWidget(values=categories),
                        description = 'Standardkategorie des Items'
                )
    comment = SchemaNode(String(),
                        widget = widget.TextInputWidget(size=40),
                        missing='',
                        description = 'Kommentar zum Item')
    title='Neues Item'

    def update(self):
        categories = self.db.getAllCategories()
        categories = [(cat, cat) for (cat, comment) in categories]
        self['category'].widget = widget.SelectWidget(values=categories)

class CategorySchema(MappingSchema):
    name  = SchemaNode(String(),
                        description = 'Name der Kategorie')
    comment = SchemaNode(String(),
                        widget = widget.TextInputWidget(size=40),
                        missing='',
                        description = 'Kommentar zur Kategorie')
    title='Neue Kategorie'

    def update(self):
        pass

class PositionSchema(MappingSchema):
    db = sqlite()
    categories = db.getAllCategories()
    categories = [(cat, cat) for (cat, comment) in categories]
    allItems = db.getAllItems()
    optgroups = defaultdict(lambda: [],{})
    for (itemid, name, category, comment) in allItems:
        optgroups[category].append((itemid, name))
    items = [widget.OptGroup(category, *values) for category, values in sorted(optgroups.items())]
    quantity = SchemaNode(
                Integer(),
                default=1
    )
    item_id  = SchemaNode(
                String(),
                widget=widget.SelectWidget(values=items),
                description = 'Item'
                )
    category = SchemaNode(
                String(),
                widget=widget.SelectWidget(values=categories),
                        description = 'Name der Kategorie'
                )
    price    = SchemaNode(
                Decimal(),
                widget=widget.MoneyInputWidget()
                )
    ean   = SchemaNode(String(),
                        missing='',
                        description = 'EAN')
    tags     = SchemaNode(String(),
                missing='',
                description = 'tags'
                )
    name = 'position'

    def update(self):
        allItems = self.db.getAllItems()
        optgroups = defaultdict(lambda: [],{})
        for (itemid, name, category, comment) in allItems:
            optgroups[category].append((itemid, name))
        items = [widget.OptGroup(category, *values) for category, values in sorted(optgroups.items())]
        self['item_id'].widget = widget.SelectWidget(values=items)
        categories = self.db.getAllCategories()
        categories = [(cat, cat) for (cat, comment) in categories]
        self['category'].widget = widget.SelectWidget(values=categories)

class PositionsSchema(SequenceSchema):
    position = PositionSchema()

    def update(self):
        self['position'].update()


class PurchaseSchema(MappingSchema):
    db = sqlite()
    categories = db.getAllCategories()
    categories = [(cat, cat) for (cat, comment) in categories]
    availableFlags = (
            ('L', 'Ledger'),
    )
    shop = SchemaNode(String(),
                        description = 'Shop')
    payment_method = SchemaNode(
                String(),
                widget=widget.SelectWidget(values=categories),
                        description = 'Bezahlmethode'
                )
    date = SchemaNode(Date(),
                      description = 'Rechnungsdatum')
    flags = SchemaNode(colander.Set(),
                       widget=widget.CheckboxChoiceWidget(values=availableFlags),
                       )
    positions = PositionsSchema()
    title='Neue Transaktion'

    def update(self):
        categories = self.db.getAllCategories()
        categories = [(cat, cat) for (cat, comment) in categories]
        self['payment_method'].widget = widget.SelectWidget(values=categories)
        self['positions'].update()




def getFormHTML():
    itemSchema = ItemSchema()
    itemForm = Form(itemSchema, buttons=('submit',),  formid='itemForm', counter=counter)
    categorySchema = CategorySchema()
    categoryForm = Form(categorySchema, buttons=('submit',), formid='categoryForm', counter=counter)
    purchaseSchema = PurchaseSchema()
    purchaseForm = Form(purchaseSchema, buttons=('submit',), formid='purchaseForm', counter=counter)
    html = []
    for form in itemForm, categoryForm, purchaseForm:
        form.schema.update()
        html.append(form.render())
    html = ''.join(html)
    return {'form':html}


@view_config(route_name='item')
def handleItemForms(request):
    db = sqlite()
    pprint.pprint(request.params)
    db.addItem(request.params)
    return {'form': ''}


@view_config(route_name='category')
def handleCategoryForms(request):
    db = sqlite()
    pprint.pprint(request.params)
    db.addCategory(request.params)
    categories = db.getAllCategories()
    categories = [(cat, cat) for (cat, comment) in categories]
    return Response(json.dumps(categories))


@view_config(route_name='entry_route')
def form_view(request):
    if request.method == 'GET':
        return getFormHTML()
    if request.method == 'PUT':
        if request.params['form'] == 'itemForm':
            # FIXME: Validation!
            return handleItemForms(request)
        if request.params['form'] == 'categoryForm':
            # FIXME: Validation!
            return handleCategoryForms(request)
    itemSchema = ItemSchema()
    itemForm = Form(itemSchema, buttons=('submit',),  formid='itemForm', counter=counter)
    categorySchema = CategorySchema()
    categoryForm = Form(categorySchema, buttons=('submit',), formid='categoryForm', counter=counter)
    purchaseSchema = PurchaseSchema()
    purchaseForm = Form(purchaseSchema, buttons=('submit',), formid='purchaseForm', counter=counter)
    db = sqlite()
    dbfunctions = {
        'itemForm': {'add': db.addItem},
        'categoryForm': {'add':db.addCategory},
        'purchaseForm': {'add':db.addPurchase}
    }
    html = []
    if 'submit' in request.POST:
        posted_formid = request.POST['__formid__']
        for (formid, form) in [('itemForm', itemForm), ('categoryForm', categoryForm), ('purchaseForm', purchaseForm)]:
            if formid == posted_formid:
                controls = list(request.POST.items())
                pstruct = peppercorn.parse(controls)
                try:
                    form.validate(controls)
                    pprint.pprint(pstruct)
                    dbAdd = dbfunctions.get(formid).get('add')
                    dbAdd(pstruct)
                    url = request.application_url
                    return HTTPFound(location=url)
                except ValidationFailure as e:
                    return {'form':e.render()}
            else:
                form.schema.update()
                html.append(form.render())
    else:
        for form in itemForm, categoryForm, purchaseForm:
            form.schema.update()
            html.append(form.render())
    html = ''.join(html)
    return {'form':html}
