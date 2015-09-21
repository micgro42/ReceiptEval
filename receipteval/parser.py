# -*- coding: utf-8 -*-
'''
Created on Nov 30, 2014

@author: Michael Große <mic.grosse@posteo.de>
'''
import csv
from receipteval.receiptCollection import receiptCollection
from receipteval.purchase import Purchase
from receipteval.item_cat_dict import ItemCategoryDict
from receipteval.helper import validate_date


class parser(object):
    '''
    classdocs
    '''

    def __init__(self, *args, **kwargs):
        '''
        Constructor
        '''
        self.dictionary = kwargs.get('category_dictionary', ItemCategoryDict())
        self.purchaseIsActive = False
        self.rc = receiptCollection()

    def __enter__(self):
        return self

    def __exit__(self, thetype, value, traceback):
        pass

    def checkLineEmptyEnough(self, line):
        return line[0] is '' and line[2] is '' and line[3] is ''

    def checkPurchaseHeader(self, line):
        return line[0] is not '' and line[2] is not ''

    def startNewPurchase(self, line):
        date = validate_date(line[0])
        self.purchaseIsActive = True
        payment_method = line[3]
        if payment_method is '':
            payment_method = 'cash'
        self.rc.purchases.append(Purchase(date=date,
                                          shop=line[2],
                                          category_dict=self.dictionary,
                                          payment_method=payment_method,
                                          flags=line[1]))

    def handleOutOfPurchaseLine(self, line):
        if self.checkLineEmptyEnough(line):
            return

        if self.checkPurchaseHeader(line):
            self.startNewPurchase(line)
        else:
            raise RuntimeError('file badly formatted: ' + str(line))

    def handleInPurchaseLine(self, line):
        if self.checkLineEmptyEnough(line):
            self.purchaseIsActive = False
            return
        if line[0] is not '':
            raise RuntimeError('file badly formatted: ' + str(line))
        if line[3] is '':
            self.rc.unsane_items.append(line[2])
        else:
            self.rc.purchases[-1].addItem(name=line[2],
                                          price=line[3],
                                          count=line[1],
                                          category=line[4])

    def readFile(self, file_path):
        with open(file_path, 'r') as receipt_file:
            csv_reader = csv.reader(receipt_file)
            firstLine = True
            for line in csv_reader:
                if firstLine:
                    firstLine = False
                    continue

                if self.purchaseIsActive:
                    self.handleInPurchaseLine(line)
                else:
                    self.handleOutOfPurchaseLine(line)

        return self.rc
