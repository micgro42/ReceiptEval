# -*- coding: utf-8 -*-
"""
provide class item_category_dict
"""
from __future__ import print_function
import os
import sys
import csv
from collections import OrderedDict


class ItemCategoryDict(object):
    """
    Set the category for every item
    """

    def __init__(self, **kwargs):
        file_path = kwargs.get('path', 'KinEtCategories.csv')
        self.item_category_dict = {}
        self.item_comment_dict = {}
        if os.path.isfile(file_path):
            self.read_categories(file_path)
        else:
            pass

        if os.path.isfile('categories.ini'):
            pass

    def read_categories(self, file_path):
        '''
        Read existing categories file
        '''
        if os.path.isfile(file_path):
            with open(file_path, 'r') as category_file:
                csv_reader = csv.reader(category_file)
                for rows in csv_reader:
                    try:
                        self.item_category_dict[rows[0].strip()] = rows[1].strip()
                    except IndexError:
                        continue
                    try:
                        if rows[2].strip() is not "":
                            self.item_comment_dict[rows[0].strip()] = rows[2].strip()
                    except IndexError:
                        continue

    def get_category(self, item):
        """Return the category of an item

        :param item: name of item
        :type item: string
        """
        return self.item_category_dict.get(item, '')

    def update_cat_file(self, receipt_path, category_path=None):
        '''
        update an existing categories file or create a new one

        :param receipt_path: name of receipt collection file
        :type receipt_path: string
        :param category_path: name of categpry file to be updated
        :type category_path: string
        '''
        if category_path and os.path.isfile(category_path):
            self.item_category_dict = {}
            self.read_categories(category_path)
        else:
            category_path = 'new_dict.csv'
        self.extract_new_categories(receipt_path)
        with open(category_path, 'w') as category_file:
            csv_writer = csv.writer(category_file, lineterminator='\n')
            ordered_categories = OrderedDict(sorted(self.item_category_dict.items(), key=lambda t: (t[1], t[0])))
            for key, value in ordered_categories.items():
                if key in self.item_comment_dict:
                    comment = self.item_comment_dict[key]
                else:
                    comment = ""
                csv_writer.writerow([key, value, comment])

    def extract_new_categories(self, file_path):
        '''
        Extract categories not yet in the categories file

        :param file_path: name of receipt collection file
        :type file_path: string
        '''
        if os.path.isfile(file_path):
            with open(file_path, 'r') as receipt_file:
                csv_reader = csv.reader(receipt_file)
                first_row = True
                for rows in csv_reader:
                    if first_row:
                        first_row = False
                        continue
                    if not rows[2]:
                        continue
                    if not rows[4]:
                        continue
                    if rows[2] not in self.item_category_dict:
                        self.item_category_dict[rows[2].strip()] = rows[4].strip()
                        continue
                    if self.item_category_dict[rows[2].strip()] != rows[4].strip():
                        print (rows[2].strip() + " has two different categories: " +
                               rows[4].strip() + " and " +
                               self.item_category_dict[rows[2].strip()], file=sys.stderr)
