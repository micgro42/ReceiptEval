# encoding: utf-8
'''
Created on Apr 19, 2015

@author: Michael Große <mic.grosse@posteo.de>
'''

from receipteval.receipt_collection import ReceiptCollection
from receipteval.purchase import Purchase
from collections import namedtuple


def test_category_correct():
    rC = ReceiptCollection()
    rC.category_dict.item_category_dict = {'Pfand': 'Pfand',
                                           'Pesto': 'Pesto',
                                           'Parmesan': 'Käse',
                                           'Heumilch': 'Milch',
                                           'Milch': 'Milch',
                                          }
    rC.check_category('Milch', 'Heumilch')
    assert not rC.unsane_categories


def test_category_wrong():
    rC = ReceiptCollection()
    rC.category_dict.item_category_dict = {'Pfand': 'Pfand',
                                           'Pesto': 'Pesto',
                                           'Parmesan': 'Käse',
                                           'Heumilch': 'Milch',
                                           'Milch': 'Milch',
                                          }
    rC.check_category('Obst', 'Heumilch')
    assert rC.unsane_categories[0] == ('Heumilch', 'Obst', 'Milch')


def test_category_missing():
    rC = ReceiptCollection()
    rC.category_dict.item_category_dict = {'Pfand': 'Pfand',
                                           'Pesto': 'Pesto',
                                           'Parmesan': 'Käse',
                                           'Heumilch': 'Milch',
                                           'Milch': 'Milch',
                                          }
    rC.check_category('', 'Heumilch')
    assert rC.unsane_categories[0] == ('Heumilch', '', 'Milch')


def test_category_stored_missing():
    rC = ReceiptCollection()
    rC.check_category('Testcategory', 'Testitem')
    assert rC.unsane_categories[0] == ('Testitem', 'Testcategory', '')


def test_category_both_missing():
    rC = ReceiptCollection()
    rC.check_category('', 'Testitem')
    assert not rC.unsane_categories


def test_create_ledger():
    receipt_collection = ReceiptCollection()
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
    receipt_collection.purchases.append(testPurchaseOne)
    testPurchaseTwo = Purchase('2015-11-28',
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
    receipt_collection.purchases.append(testPurchaseTwo)
    testPurchaseThree = Purchase('2015-11-30',
                                 "TestShopThree",
                                 payment_method="Giro")
    testPurchaseThree.positions.append(Position('bar',
                                                'category:subcategory2',
                                                4.56,
                                                '',
                                                ''))
    testPurchaseThree.positions.append(Position('foo',
                                                'category:subcategory1',
                                                2.46,
                                                '2',
                                                ''))
    receipt_collection.purchases.append(testPurchaseThree)

    actual_output = receipt_collection.get_ledger()
    expected_output = "2015-11-28 TestShopTwo\n"
    expected_output += "  Aktiva:Giro  -7.02\n"
    expected_output += "  category:subcategory2  4.56\n"
    expected_output += "  category:subcategory1  2.46\n"
    expected_output += "\n"
    expected_output += "2015-11-29 TestShopOne\n"
    expected_output += "  Aktiva:Portmonaie  -1.23\n"
    expected_output += "  category:subcategory1  1.23\n"
    expected_output += "\n"
    expected_output += "2015-11-30 TestShopThree\n"
    expected_output += "  Aktiva:Giro  -7.02\n"
    expected_output += "  category:subcategory2  4.56\n"
    expected_output += "  category:subcategory1  2.46\n"
    expected_output += "\n"
    assert expected_output == actual_output
