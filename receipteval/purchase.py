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
        self.total = 0.0

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def addItem(self, name, price, count, **kwargs):
        Item = namedtuple('item', ['name','category','price','count','weight'])
        weight = kwargs.get('weight','')
        category = kwargs.get('category','')
        stored_category = self.category_dict.getCategory(name)
        if category is '' and stored_category is not '':
            category = stored_category
        try:
            price = float(price)
            self.total += price
        except ValueError:
            print 'Price: ' + price
            print 'Name: ' + name
            raise
        self.positions.append(Item(name,category,price,count,weight))

    def printLegacy(self):
        pass

    def printLedger(self):
        pass
