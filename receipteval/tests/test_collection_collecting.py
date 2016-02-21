# encoding: utf-8
'''
@author: Michael Große <mic.grosse@posteo.de>
@repository: https://github.com/micgro42/ReceiptEval
'''

import pytest
from receipteval.receipt_collection import ReceiptCollection
from receipteval.purchase import Purchase


@pytest.fixture()  # Registering this function as a fixture.
def purchase_list_fixture(request):
    purchase_list = []
    test_purchase1 = Purchase('2015-11-29', 'Bio Company')
    test_purchase1.add_item(name='Blanc de Pomm',
                            price=1.69,
                            count=1,
                            category='Zubrot')
    test_purchase1.add_item('Seidentofu', 5.18, 2)
    purchase_list.append(test_purchase1)

    test_purchase2 = Purchase('2014-11-01', 'Bio Company')
    test_purchase2.add_item('Risotto', 4.38, 2, category='Kochzutaten')
    test_purchase2.add_item('Sesam', 3.69, 1)
    test_purchase2.add_item('Cashewbruch', 10.99, 1)
    test_purchase2.add_item('Bananen', 1.22, 1, category='Obst')
    test_purchase2.add_item('Roggenmehl', 3.98, 2, category='Mehl')
    test_purchase2.add_item('Walnusskerne', 3.49, 1)
    test_purchase2.add_item('Datteln', 5.29, 1)
    test_purchase2.add_item('Safranfäden', 6.29, 1, category='Gewürze')
    test_purchase2.add_item('Vanillepulver', 2.49, 1, category='Gewürze')
    test_purchase2.add_item('Kakaopulver', 2.19, 1)
    test_purchase2.add_item('Basilikum, frisch', 1.99, 1, category='Gewürze')
    test_purchase2.add_item('Item without Price', '', 1, category='Mehl')
    test_purchase2.add_item('Roggenmehl', 3.98, 2, category='Obst')
    purchase_list.append(test_purchase2)

    test_purchase3 = Purchase('2015-11-17',
                              'Übertrag',
                              payment_method='Giro',
                              flags='L')
    test_purchase3.add_item('Abhebung', 100, 1, category='Aktiva:Portmonaie')
    purchase_list.append(test_purchase3)

    return purchase_list


def test_collect_unsane_items(purchase_list_fixture):
    rc = ReceiptCollection(purchase_list_fixture)
    rc.collect_items()
    assert rc.unsane_items == ['Item without Price', 'Roggenmehl']


def test_categories(purchase_list_fixture):
    receipt_collection = ReceiptCollection(purchase_list_fixture)
    receipt_collection.collect_items()
    assert sorted(['Zubrot',
                   '',
                   'Mehl',
                   'Kochzutaten',
                   'Obst',
                   'Gewürze'
                   ]) == sorted(receipt_collection.categories.keys())


def test_items_in_categories(purchase_list_fixture):
    rc = ReceiptCollection(purchase_list_fixture)
    rc.collect_items()
    assert sorted(rc.categories[''][1]) == sorted(['Kakaopulver',
                                                   'Seidentofu',
                                                   'Sesam',
                                                   'Cashewbruch',
                                                   'Datteln',
                                                   'Walnusskerne'])
    assert sorted(rc.categories['Zubrot'][1]) == sorted(['Blanc de Pomm'])
    assert sorted(rc.categories['Gewürze'][1]) == sorted(['Safranfäden',
                                                          'Vanillepulver',
                                                          'Basilikum, frisch'])
    assert sorted(rc.categories['Mehl'][1]) == sorted(['Roggenmehl'])
    assert sorted(rc.categories['Kochzutaten'][1]) == sorted(['Risotto'])
    assert sorted(rc.categories['Obst'][1]) == sorted(['Bananen',
                                                       'Roggenmehl'])


def test_category_prices(purchase_list_fixture):
    rc = ReceiptCollection(purchase_list_fixture)
    rc.collect_items()
    assert round(rc.categories[''][0], 2) == 30.83
    assert round(rc.categories['Zubrot'][0], 2) == 1.69
    assert round(rc.categories['Mehl'][0], 2) == 3.98
    assert round(rc.categories['Kochzutaten'][0], 2) == 4.38
    assert round(rc.categories['Obst'][0], 2) == 5.20
    assert round(rc.categories['Gewürze'][0], 2) == 10.77
