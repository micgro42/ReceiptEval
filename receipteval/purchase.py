# -*- coding: utf-8 -*-
'''
Created on May 10, 2015

@author: Michael Große <mic.grosse@posteo.de>
'''

from collections import namedtuple

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
        self.total = 0.0

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def addItem(self, name, price, count, **kwargs):
        Item = namedtuple('item', ['name','category','price','count','weight'])
        self.positions.append(Item(name,'',price,count,''))
        self.total += price
        pass

    def printLedger(self):
        pass
