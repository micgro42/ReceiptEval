# -*- coding: utf-8 -*-
'''
Created on May 10, 2015

@author: Michael Große <mic.grosse@posteo.de>
'''
from __future__ import print_function
from logging import warning
from collections import namedtuple
from receipteval.item_cat_dict import ItemCategoryDict
from receipteval.helper import validate_date


class Purchase(object):
    '''
    Hold the information of one receipt
    '''

    def __init__(self, date, shop, **kwargs):
        self._date = None
        self.date = date
        self.shop = shop
        self.payment_method = kwargs.get('payment_method', 'cash')
        self._positions = []
        self.category_dict = kwargs.get('category_dict', ItemCategoryDict())
        self._total = 0.0
        self.flags = {}
        self.extract_flags(kwargs.get('flags', ''))
        self.unsane_items = []

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        pass

    def extract_flags(self, flags):
        '''
        Parse the flags for the purchase
        @todo: This should use binary flags
        '''
        if flags is 'L':
            self.flags['ledger'] = True
        else:
            self.flags['ledger'] = False

    @property
    def positions(self):
        '''
        If this is a ledger-only purchase, return nothing
        '''
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

    def add_item(self, name, price, count, **kwargs):
        '''
        Add a position to the purchase.
        '''
        item = namedtuple('item', ['name', 'category', 'price', 'count', 'weight'])
        weight = kwargs.get('weight', '')
        category = kwargs.get('category', '')
        stored_category = self.category_dict.get_category(name)
        if category is '' and stored_category is not '':
            category = stored_category
        try:
            price = float(price)
        except ValueError:
            warning('price missing ' + name)
            if (price is not ''):
                raise
            self.unsane_items.append(name)
        else:
            self.positions = item(name, category, price, count, weight)

    def get_ledger(self):
        '''
        Return this purchase in the format used for github.com/ledger/ledger
        '''
        ledger_string = ""
        ledger_string += self.date + " " + self.shop + "\n"
        if self.payment_method == "Giro":
            ledger_string += "  Aktiva:Giro  " + str(-self.total) + "\n"
        elif self.payment_method == "cash":
            ledger_string += "  Aktiva:Portmonaie  " + str(-self.total) + "\n"
        else:
            ledger_string += "  " + self.payment_method + "  " + str(-self.total) + "\n"
        for position in self._positions:
            ledger_string += "  " + position.category + "  " + str(position.price) + "\n"
        ledger_string += "\n"
        return ledger_string
