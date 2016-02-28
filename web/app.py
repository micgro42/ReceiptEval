#!/usr/bin/env python

import os

from wsgiref.simple_server import make_server
from pyramid.config import Configurator

from colander import MappingSchema
from colander import SequenceSchema
from colander import SchemaNode
from colander import String
from colander import Date
from colander import Decimal
from colander import Integer
from colander import Length
from colander import OneOf
from colander import null
import colander

from deform import ValidationFailure
from deform import Form
from deform import widget

import peppercorn
import itertools

from receipteval.storage.sqlite import sqlite



here = os.path.dirname(os.path.abspath(__file__))

counter = itertools.count()

class ItemSchema(MappingSchema):
    name  = SchemaNode(String(),
                        description = 'Name des Items')
    comment = SchemaNode(String(),
                        widget = widget.TextInputWidget(size=40),
                        missing='',
                        description = 'Kommentar zum Item')
    ean   = SchemaNode(String(),
                        missing='',
                        description = 'EAN')

class CategorySchema(MappingSchema):
    name  = SchemaNode(String(),
                        description = 'Name der Kategorie')
    comment = SchemaNode(String(),
                        widget = widget.TextInputWidget(size=40),
                        missing='',
                        description = 'Kommentar zur Kategorie')

class PositionSchema(MappingSchema):
    db = sqlite()
    categories = db.getAllCategories()
    categories = [(cat, cat) for (cat, comment) in categories]
    items = db.getAllItems()
    items = [(itemid, name) for (itemid, name, ean, comment) in items]
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
    tags     = SchemaNode(String(),
                missing='',
                description = 'tags'
                )

    def update(self):
        items = self.db.getAllItems()
        items = [(itemid, name) for (itemid, name, ean, comment) in items]
        self['item_id'].widget = widget.SelectWidget(values=items)
        categories = self.db.getAllCategories()
        categories = [(cat, cat) for (cat, comment) in categories]
        self['category'].widget = widget.SelectWidget(values=categories)

class PositionsSchema(colander.SequenceSchema):
    position = PositionSchema()

    def update(self):
        print(self.__dict__)
        print(dir(self['abc']))
        self['abc'].update()


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

    def update(self):
        categories = self.db.getAllCategories()
        categories = [(cat, cat) for (cat, comment) in categories]
        self['payment_method'].widget = widget.SelectWidget(values=categories)
        # print(self.__dict__)
        # print(dir(self['positions']))
        self['positions'].update()

def form_view(request):
    itemSchema = ItemSchema()
    itemForm = Form(itemSchema, buttons=('submit',),  formid='itemForm', counter=counter)
    categorySchema = CategorySchema()
    categoryForm = Form(categorySchema, buttons=('submit',), formid='categoryForm', counter=counter)

    purchaseSchema = PurchaseSchema()
    purchaseSchema.update()
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
                controls = request.POST.items()
                pstruct = peppercorn.parse(controls)
                print(pstruct)
                try:
                    form.validate(controls)
                    dbAdd = dbfunctions.get(formid).get('add')
                    dbAdd(pstruct)
                    html.append(form.render(null))
                except ValidationFailure as e:
                    return {'form':e.render()}
            else:
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
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()

