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
        if os.path.isfile(file_path):
            self.item_category_dict = {}
            with open(file_path, 'r') as receipt_file:
                csv_reader = csv.reader(receipt_file)
                self.item_category_dict = {rows[0].strip():rows[1].strip() for rows in csv_reader}
        if os.path.isfile('categories.ini'):
            pass

    def getCategory(self, item):
        """Return the category of an item

        :param item: name of item
        :type item: string
        """
        return self.item_category_dict.get(item,'')

    def extractNew(self, path):
        """ Create new categories file from receipt collection
 
        :param path: name of receipt collection file
        :type path: string
        """
        pass
