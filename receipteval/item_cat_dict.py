# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys
import csv
from collections import OrderedDict


"""
provide class item_category_dict
"""
class ItemCategoryDict(object):
    """
    Set the category for every item

    """

    def __init__(self):
        file_path = 'KinEtCategories.csv'
        self.item_category_dict = {}
        if os.path.isfile(file_path):
            with open(file_path, 'r') as category_file:
                csv_reader = csv.reader(category_file)
                self.item_category_dict = {rows[0].strip():rows[1].strip() for rows in csv_reader}
        if os.path.isfile('categories.ini'):
            pass

    def getCategory(self, item):
        """Return the category of an item

        :param item: name of item
        :type item: string
        """
        return self.item_category_dict.get(item,'')

    def updateCatFile(self, receipt_path, category_path = None):
        if category_path and os.path.isfile(category_path):
            self.item_category_dict = {}
            self.read_categories(category_path)
        else:
            category_path = 'new_dict.csv'
        self.extractNew(receipt_path)
        with open(category_path, 'wb') as category_file:
            csv_writer = csv.writer(category_file)
            ordered_categories=OrderedDict(sorted(self.item_category_dict.items(), key=lambda t: (t[1],t[0])))
            for key, value in ordered_categories.items():
                csv_writer.writerow([key, value])

    def extractNew(self, file_path):
        """ Create new categories file from receipt collection
 
        :param file_path: name of receipt collection file
        :type file_path: string
        """
        if os.path.isfile(file_path):
            with open(file_path, 'r') as receipt_file:
                csv_reader = csv.reader(receipt_file)
                for rows in csv_reader:
                    if not rows[2]:
                        continue
                    if not rows[4]:
                        continue
                    if rows[2] not in self.item_category_dict:
                        self.item_category_dict[rows[2].strip()] = rows[4].strip()
                        continue
                    if self.item_category_dict[rows[2].strip()] != rows[4].strip():
                        print (rows[2].strip() + " has two different categories: "
                                + rows[4].strip() + " and "
                                + self.item_category_dict[rows[2].strip()], file=sys.stderr)

