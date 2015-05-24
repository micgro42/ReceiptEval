# -*- coding: utf-8 -*-
'''
Created on Nov 30, 2014

@author: Michael Große <mic.grosse@posteo.de>
'''
from collections import defaultdict
from item_cat_dict import ItemCategoryDict

class receiptCollection(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.categories = defaultdict(lambda : [0.0,set()])
        self.receipt_lines = []
        self.purchases = []
        self.unsane_items = []
        self.unsane_categories = []
        self.categoryDict = ItemCategoryDict()

    def collectItems(self):
        for purchase in self.purchases:
            for item in purchase.positions:
                self.categories[item.category][1].add(item.name)
                self.categories[item.category][0] += item.price

        self.checkSanity()
        self.calcTotal()


    def checkCategory(self, c, item):
        storedCategory = self.categoryDict.getCategory(item)
        if (c != storedCategory):
            self.unsane_categories.append((item, c, storedCategory))

    def checkSanity(self):
        all_items = set()
        for c in self.categories:
            if c is '':
                continue
            for item in self.categories[c][1]:
                if (item in all_items):
                    self.unsane_items.append(item)
                self.checkCategory(c, item)
                all_items.add(item)

    def calcTotal(self):
        self.total = 0.0
        for c in self.categories:
            self.total += self.categories[c][0]
