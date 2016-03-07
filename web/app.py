#!/usr/bin/env python

import os

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPFound

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

from receipteval.storage.sqlite import sqlite

import pprint

here = os.path.dirname(os.path.abspath(__file__))

counter = itertools.count()

class ItemSchema(MappingSchema):
    name  = SchemaNode(String(),
                        description = 'Bezeichnung des Items',
                        title='Name')
    comment = SchemaNode(String(),
                        widget = widget.TextInputWidget(size=40),
                        missing='',
                        description = 'Kommentar zum Item')
    title='Neues Item'

    def update(self):
        pass

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
    items = db.getAllItems()
    items = [(itemid, name) for (itemid, name, comment) in items]
    quantity = SchemaNode(
                Integer()
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

    def update(self):
        items = self.db.getAllItems()
        items = [(itemid, name) for (itemid, name, comment) in items]
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

def form_view(request):
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
            html.append(form.render())
    html = ''.join(html)
    return {'form':html}

if __name__ == '__main__':
    settings = dict(reload_templates=True)
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_view(form_view, renderer=os.path.join(here, 'form.pt'))
    config.add_static_view('static', 'deform:static')
    config.add_static_view('js', path='js')
    config.add_static_view('css', path='css')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()

