# -*- coding: utf-8 -*-
import os
import csv

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
                    self.item_category_dict[rows[2].strip()] = rows[4].strip()
                print self.item_category_dict
