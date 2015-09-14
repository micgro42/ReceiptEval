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

    def __enter__(self):
        return self

    def __exit__(self, thetype, value, traceback):
        pass

    def readFile(self, file_path):
        rc = receiptCollection()
        purchaseIsActive = False
        with open(file_path, 'r') as receipt_file:
            csv_reader = csv.reader(receipt_file)
            firstLine = True
            for line in csv_reader:
                if firstLine:
                    firstLine = False
                    continue

                # empty lines: end purchase and otherwise skip
                if line[0] is '' and line[2] is '' and line[3] is '':
                    purchaseIsActive = False
                    continue

                date = line[0]

                # only the heading of a purchase should have content in the
                # date field
                if purchaseIsActive and date is not '':
                    raise RuntimeError('file badly formatted: ' + str(line))

                # start a new purchase and then read the next line
                if date is not '' and not purchaseIsActive:
                    date = validate_date(date_text=date)
                    purchaseIsActive = True
                    payment_method = line[3]
                    if payment_method is '':
                        payment_method = 'cash'
                    rc.purchases.append(Purchase(date=date,
                                                 shop=line[2],
                                                 category_dict=self.dictionary,
                                                 payment_method=payment_method,
                                                 flags=line[1]))

                    continue

                quantity = line[1]
                name = line[2]
                price = line[3]
                category = line[4]
                if not purchaseIsActive and (name is '' or price is '' or date is ''):
                    raise RuntimeError('file badly formatted: ' + str(line))

                if price is '':
                    rc.unsane_items.append(name)
                else:
                    rc.purchases[-1].addItem(name,
                                             price,
                                             quantity,
                                             category=category)

        return rc
