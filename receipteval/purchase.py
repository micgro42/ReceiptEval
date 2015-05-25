# -*- coding: utf-8 -*-
'''
Created on May 10, 2015

@author: Michael Große <mic.grosse@posteo.de>
'''

from collections import namedtuple
from receipteval.item_cat_dict import ItemCategoryDict

class Purchase(object):
    '''
    classdocs
    '''


    def __init__(self, date, shop, *args, **kwargs):
        '''
        Constructor
        '''
        self.date = date
        self.shop = shop
        self.payment_method = kwargs.get('payment_method','cash')
        self.positions = []
        self.category_dict = kwargs.get('category_dict',ItemCategoryDict())
        self._total = 0.0

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @property
    def total(self):
        self._total = 0.0
        for item in self.positions:
            self._total += item.price
        return self._total

    def addItem(self, name, price, count, **kwargs):
        Item = namedtuple('item', ['name','category','price','count','weight'])
        weight = kwargs.get('weight','')
        category = kwargs.get('category','')
        stored_category = self.category_dict.getCategory(name)
        if category is '' and stored_category is not '':
            category = stored_category
        try:
            price = float(price)
        except ValueError:
            print 'Price: ' + price
            print 'Name: ' + name
            raise
        self.positions.append(Item(name,category,price,count,weight))

    def getLedger(self):
        ledgerString = ""
        ledgerString += self.date + " " + self.shop + "\n"
        if self.payment_method == "Giro":
            ledgerString += "  Aktiva:Giro  " + str(-self.total) + "\n"
        else:
            ledgerString += "  Aktiva:Portmonaie  " + str(-self.total) + "\n"
        for position in self.positions:
            ledgerString += "  " + position.category + "  " + str(position.price) + "\n"
        ledgerString += "\n"
        return ledgerString


    def printLegacy(self):
        pass
