# -*- coding: utf-8 -*-
'''
Created on May 10, 2015

@author: Michael Große <mic.grosse@posteo.de>
'''
from __future__ import print_function
from collections import namedtuple
from receipteval.item_cat_dict import ItemCategoryDict
from receipteval.helper import validate_date


class Purchase(object):
    '''
    classdocs
    '''

    def __init__(self, date, shop, **kwargs):
        '''
        Constructor
        '''
        self._date = None
        self.date = date
        self.shop = shop
        self.payment_method = kwargs.get('payment_method', 'cash')
        self._positions = []
        self.category_dict = kwargs.get('category_dict', ItemCategoryDict())
        self._total = 0.0
        self.flags = {}
        self.extractFlags(kwargs.get('flags', ''))

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        pass

    def extractFlags(self, flags):
        if flags is 'L':
            self.flags['ledger'] = True
        else:
            self.flags['ledger'] = False

    @property
    def positions(self):
        if not self.flags['ledger']:
            return self._positions
        else:
            return []

    @positions.setter
    def positions(self, value):
        self._positions.append(value)

    @property
    def total(self):
        self._total = 0.0
        for item in self._positions:
            self._total += item.price
        return self._total

    @property
    def date(self):
        return self._date.strftime('%Y-%m-%d')

    @date.setter
    def date(self, value):
        self._date = validate_date(value)

    def addItem(self, name, price, count, **kwargs):
        Item = namedtuple('item', ['name', 'category', 'price', 'count', 'weight'])
        weight = kwargs.get('weight', '')
        category = kwargs.get('category', '')
        stored_category = self.category_dict.getCategory(name)
        if category is '' and stored_category is not '':
            category = stored_category
        try:
            price = float(price)
        except ValueError:
            print ('Price: ' + price)
            print ('Name: ' + name)
            raise
        self.positions = Item(name, category, price, count, weight)

    def getLedger(self):
        ledgerString = ""
        ledgerString += self.date + " " + self.shop + "\n"
        if self.payment_method == "Giro":
            ledgerString += "  Aktiva:Giro  " + str(-self.total) + "\n"
        elif self.payment_method == "cash":
            ledgerString += "  Aktiva:Portmonaie  " + str(-self.total) + "\n"
        else:
            ledgerString += "  " + self.payment_method + "  " + str(-self.total) + "\n"
        for position in self._positions:
            ledgerString += "  " + position.category + "  " + str(position.price) + "\n"
        ledgerString += "\n"
        return ledgerString

    def printLegacy(self):
        pass
