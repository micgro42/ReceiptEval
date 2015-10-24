# encoding: utf-8
'''
Created on Apr 19, 2015

@author: Michael Große <mic.grosse@posteo.de>
'''

from receipteval.receiptCollection import receiptCollection
from receipteval.purchase import Purchase
from collections import namedtuple


def test_category_correct():
    rC = receiptCollection()
    rC.categoryDict.item_category_dict = {'Pfand': 'Pfand',
                                          'Pesto': 'Pesto',
                                          'Parmesan': 'Käse',
                                          'Heumilch': 'Milch',
                                          'Milch': 'Milch',
                                          }
    rC.checkCategory('Milch', 'Heumilch')
    assert not rC.unsane_categories


def test_category_wrong():
    rC = receiptCollection()
    rC.categoryDict.item_category_dict = {'Pfand': 'Pfand',
                                          'Pesto': 'Pesto',
                                          'Parmesan': 'Käse',
                                          'Heumilch': 'Milch',
                                          'Milch': 'Milch',
                                          }
    rC.checkCategory('Obst', 'Heumilch')
    assert rC.unsane_categories[0] == ('Heumilch', 'Obst', 'Milch')


def test_category_missing():
    rC = receiptCollection()
    rC.categoryDict.item_category_dict = {'Pfand': 'Pfand',
                                          'Pesto': 'Pesto',
                                          'Parmesan': 'Käse',
                                          'Heumilch': 'Milch',
                                          'Milch': 'Milch',
                                          }
    rC.checkCategory('', 'Heumilch')
    assert rC.unsane_categories[0] == ('Heumilch', '', 'Milch')


def test_category_stored_missing():
    rC = receiptCollection()
    rC.checkCategory('Testcategory', 'Testitem')
    assert rC.unsane_categories[0] == ('Testitem', 'Testcategory', '')


def test_category_both_missing():
    rC = receiptCollection()
    rC.checkCategory('', 'Testitem')
    assert not rC.unsane_categories


def test_create_ledger():
    rc = receiptCollection()
    Position = namedtuple('item', ['name',
                                   'category',
                                   'price',
                                   'count',
                                   'weight'])
    testPurchaseOne = Purchase('2015-11-29', "TestShopOne")
    testPurchaseOne.positions.append(Position('foo',
                                              'category:subcategory1',
                                              1.23,
                                              '',
                                              ''))
    rc.purchases.append(testPurchaseOne)
    testPurchaseTwo = Purchase('2015-11-29',
                               "TestShopTwo",
                               payment_method="Giro")
    testPurchaseTwo.positions.append(Position('bar',
                                              'category:subcategory2',
                                              4.56,
                                              '',
                                              ''))
    testPurchaseTwo.positions.append(Position('foo',
                                              'category:subcategory1',
                                              2.46,
                                              '2',
                                              ''))
    rc.purchases.append(testPurchaseTwo)
    actual_output = rc.getLedger()
    expected_output = "2015-11-29 TestShopOne\n"
    expected_output += "  Aktiva:Portmonaie  -1.23\n"
    expected_output += "  category:subcategory1  1.23\n"
    expected_output += "\n"
    expected_output += "2015-11-29 TestShopTwo\n"
    expected_output += "  Aktiva:Giro  -7.02\n"
    expected_output += "  category:subcategory2  4.56\n"
    expected_output += "  category:subcategory1  2.46\n"
    expected_output += "\n"
    assert expected_output == actual_output