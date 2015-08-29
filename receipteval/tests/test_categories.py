# -*- coding: utf-8 -*-
'''
Created on Apr 19, 2015

@author: Michael Große <mic.grosse@posteo.de>
'''

import unittest
from receipteval.item_cat_dict import ItemCategoryDict


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_category(self):
        category_dict = ItemCategoryDict()
        category_dict.item_category_dict = {
                                          'Pfand': 'Pfand',
                                          'Pesto': 'Pesto',
                                          'Parmesan': 'Käse',
                                          'Heumilch': 'Milch',
                                          'Milch': 'Milch',
                                          }
        cat_milch = category_dict.getCategory('Milch')
        assert cat_milch == 'Milch'


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
