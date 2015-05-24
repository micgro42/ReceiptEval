# -*- coding: utf-8 -*-
'''
Created on Nov 30, 2014

@author: Michael Große <mic.grosse@posteo.de>
'''
import csv
from receipteval.receiptCollection import receiptCollection
from numpy.f2py.auxfuncs import throw_error
from receipteval.purchase import Purchase
from receipteval.item_cat_dict import ItemCategoryDict

class parser(object):
    '''
    classdocs
    '''

    def __init__(self,*args, **kwargs):
        '''
        Constructor
        '''
        self.dictionary = kwargs.get('category_dictionary',ItemCategoryDict())

    def __enter__(self):
        return self

    def __exit__(self, thetype, value, traceback):
        pass
        #return True # todo: is this line necessary? 

    def readFile(self, file_path):
        rc = receiptCollection()
        inPurchase = False;
        with open(file_path, 'rb') as receipt_file:
            csv_reader = csv.reader(receipt_file)
            for line in csv_reader:
                date = line[0]
                if date is not '' and inPurchase:
                    raise RuntimeError('file badly formatted: ' + str(line))
                if date is not '' and not inPurchase:
                    inPurchase = True
                    rc.purchases.append(Purchase(date,line[1],category_dict = self.dictionary))
                    print 'New purchase started: ' + str(line)
                    continue
                quantity = line[1]
                name = line[2]
                price = line[3]
                category = line[4]
                if name is '' and price is '':
                    inPurchase = False
                    print 'purchase ended'
                    continue
                if not inPurchase and (name is '' or price is ''):
                    throw_error('file badly formatted')
                print 'added new item to purchase: ' + str(line)
                if price is '':
                    rc.unsane_items.append(name)
                else:
                    rc.purchases[-1].addItem(name,price,quantity,category=category)

        return rc
