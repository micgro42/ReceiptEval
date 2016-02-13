# -*- coding: utf-8 -*-
'''
Created on Nov 30, 2014

@author: Michael Große <mic.grosse@posteo.de>
'''
import csv
from receipteval.purchase import Purchase
from receipteval.item_cat_dict import ItemCategoryDict
from receipteval.helper import validate_date


class Parser(object):
    '''
    Parse csv file with receipts.
    '''

    def __init__(self, *args, **kwargs):
        self.dictionary = kwargs.get('category_dictionary', ItemCategoryDict())
        self.purchase_is_active = None
        self.active_purchase = None
        self.purchases = []

    def __enter__(self):
        return self

    def __exit__(self, thetype, value, traceback):
        pass

    def read_file(self, file_path):
        '''
        Read a csv file and parse its contents into array of purchases
        '''
        with open(file_path, 'r') as receipt_file:
            csv_reader = csv.reader(receipt_file)
            first_line = True
            for line in csv_reader:
                if first_line:
                    first_line = False
                    continue
                if self.active_purchase is None:
                    self.handle_out_of_purchase_line(line)
                else:
                    self.handle_in_purchase_line(line)
        self.clean_up()
        return self.purchases

    @staticmethod
    def check_line_empty_enough(line):
        '''
        Check that the date-, name- and price-field are empty to signal an
        empty line
        '''
        return line[0] is '' and line[2] is '' and line[3] is ''

    @staticmethod
    def check_purchase_header(line):
        '''
        Check that the date field and the shopname field are not empty.
        '''
        return line[0] is not '' and line[2] is not ''

    def start_new_purchase(self, line):
        '''
        Create and initialize new purchase object.
        '''
        date = validate_date(line[0])
        self.purchase_is_active = True
        payment_method = line[3]
        if payment_method is '':
            payment_method = 'cash'
        self.active_purchase = Purchase(date=date,
                                        shop=line[2],
                                        category_dict=self.dictionary,
                                        payment_method=payment_method,
                                        flags=line[1])

    def handle_out_of_purchase_line(self, line):
        '''
        The line must by either empty or the begin of a new purchase.
        '''
        if self.check_line_empty_enough(line):
            return

        if self.check_purchase_header(line):
            self.start_new_purchase(line)
        else:
            raise RuntimeError('file badly formatted: ' + str(line))

    def handle_in_purchase_line(self, line):
        '''
        The line should either be empty, ending the purchase or it should be
        a valid position.
        '''
        if self.check_line_empty_enough(line):
            self.purchases.append(self.active_purchase)
            self.active_purchase = None
            return
        if line[0] is not '' or line[2] is '':
            raise RuntimeError('file badly formatted: ' + str(line))
        # if line[3] is '':
        #     warning('price missing ' + line[2])
        #     @TODO: decide if we should handle a missing price in the parser
        else:
            self.active_purchase.add_item(name=line[2],
                                          price=line[3],
                                          count=line[1],
                                          category=line[4])

    def clean_up(self):
        if self.active_purchase is not None:
            self.purchases.append(self.active_purchase)
            self.active_purchase = None
