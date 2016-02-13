# -*- coding: utf-8 -*-
'''
Created on Nov 30, 2014

@author: Michael Große <mic.grosse@posteo.de>
'''
from collections import defaultdict
from receipteval.item_cat_dict import ItemCategoryDict


class ReceiptCollection(object):
    '''
    Collection of purchases with evaluation and output options.
    '''

    def __init__(self, purchases=[]):
        self.categories = defaultdict(lambda: [0.0, set()])
        self.purchases = purchases
        self.unsane_items = []
        self.unsane_categories = []
        self.category_dict = ItemCategoryDict()
        self.total = 0.0

    def collect_items(self):
        '''
        sort all positions in our stored receipts/purchases into their
        respective categories
        '''
        for purchase in self.purchases:
            self.unsane_items.extend(purchase.unsane_items)
            for item in purchase.positions:
                self.categories[item.category][1].add(item.name)
                self.categories[item.category][0] += item.price

        self.check_sanity()
        self.calculate_total()

    def check_category(self, category, item):
        '''
        make list of conflicting categories
        '''
        stored_category = self.category_dict.get_category(item)
        if category != stored_category:
            self.unsane_categories.append((item, category, stored_category))

    def check_sanity(self):
        '''
        make list of items belonging to more than one category
        '''
        all_items = set()
        for category in self.categories:
            if category is '':
                continue
            for item in self.categories[category][1]:
                if item in all_items:
                    self.unsane_items.append(item)
                self.check_category(category, item)
                all_items.add(item)

    def calculate_total(self):
        '''
        calculate the grand total across all categories
        '''
        self.total = 0.0
        for category in self.categories:
            self.total += self.categories[category][0]

    def get_ledger(self, date='1900-01-01'):
        '''
        create output in the format of the ledger application
        '''
        ledger_output = ""
        for receipt in sorted(self.purchases, key=lambda t: t.date):
            if receipt.date >= date:
                ledger_output += receipt.get_ledger()
        return ledger_output
