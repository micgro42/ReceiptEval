# encoding: utf-8
'''
Created on Nov 30, 2014

@author: Michael Große <mic.grosse@posteo.de>
'''
import pytest
import os
from receipteval.parser import parser
from receipteval.item_cat_dict import ItemCategoryDict

@pytest.fixture()  # Registering this function as a fixture.
def factory_file(request):
    with open('receipts_test.csv', 'w') as receipt_file:
        receipt_file.writelines(["29.11.,,Bio Company,,,,,,\n",
                               ",1,Blanc de Pomm,1.69,Zubrot,,,,\n",
                               ",2,Seidentofu,5.18,,,,,\n",
                               ",,,,,,,,\n",
                               "1.11.2014,,Bio Company,,,46.00,,,\n",
                               ",2,Risotto,4.38,Kochzutaten,,,,\n",
                               ",,Sesam,3.69,,,,,\n",
                               ",,Cashewbruch,10.99,,,,,\n",
                               ",,Bananen,1.22,Obst,,,,\n",
                               ",2,Roggenmehl,3.98,Mehl,,,,\n",
                               ",,Walnusskerne,3.49,,,,,\n",
                               ",,Datteln,5.29,,,,,\n",
                               ",,Safranfäden,6.29,Gewürze,,,,\n",
                               ",,Vanillepulver,2.49,Gewürze,,,,\n",
                               ",,Kakaopulver,2.19,,,,,\n",
                               ',,"Basilikum, frisch",1.99,Gewürze,,,,\n',
                               ',,Item without Price,,Mehl,,,,\n',
                               ",2,Roggenmehl,3.98,Obst,,,,\n"])
    request.addfinalizer(teardown_factory_file)

def teardown_factory_file():
    if os.path.isfile("receipts_test.csv"):
        os.remove("receipts_test.csv")


def test_readfile(factory_file):
    empty_dict = ItemCategoryDict()
    empty_dict.item_category_dict = {}
    with parser(category_dictionary = empty_dict) as p:
        rc = p.readFile('receipts_test.csv')
    assert rc.purchases[0].date == '29.11.'
    assert rc.purchases[0].shop == 'Bio Company'
    assert rc.purchases[0].positions[0].name == 'Blanc de Pomm'
    assert rc.purchases[0].positions[0].price == 1.69
    assert rc.purchases[0].positions[0].count == "1"
    assert rc.purchases[0].positions[0].category == 'Zubrot'
    assert rc.purchases[0].positions[1].name == 'Seidentofu'
    assert rc.purchases[0].positions[1].price == 5.18
    assert rc.purchases[0].positions[1].count == "2"
    assert rc.purchases[0].positions[1].category == ''




def test_categories(factory_file):
    empty_dict = ItemCategoryDict()
    empty_dict.item_category_dict = {}
    with parser(category_dictionary = empty_dict) as p:
        rc = p.readFile('receipts_test.csv')
        rc.collectItems()
    assert sorted(['Zubrot','','Mehl','Kochzutaten','Obst','Gewürze']) == sorted(rc.categories.keys())

def test_items_in_categories(factory_file):
    empty_dict = ItemCategoryDict()
    empty_dict.item_category_dict = {}
    with parser(category_dictionary = empty_dict) as p:
        rc = p.readFile('receipts_test.csv')
    rc.collectItems()
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
    assert sorted(rc.categories['Obst'][1]) == sorted(['Bananen','Roggenmehl'])

def test_category_prices(factory_file):
    empty_dict = ItemCategoryDict()
    empty_dict.item_category_dict = {}
    with parser(category_dictionary = empty_dict) as p:
        rc = p.readFile('receipts_test.csv')
    rc.collectItems()
    assert round(rc.categories[''][0],2) == 30.83
    assert round(rc.categories['Zubrot'][0],2) == 1.69
    assert round(rc.categories['Mehl'][0],2) == 3.98
    assert round(rc.categories['Kochzutaten'][0],2) == 4.38
    assert round(rc.categories['Obst'][0],2) == 5.20
    assert round(rc.categories['Gewürze'][0],2) == 10.77
    
def test_unsane_items(factory_file):
    with parser() as p:
        rc = p.readFile('receipts_test.csv')
    rc.collectItems()
    assert sorted(['Item without Price', 'Roggenmehl']) == sorted(rc.unsane_items)


def test_category_create(factory_file):
    category_dict = ItemCategoryDict()
    category_dict.item_category_dict = {}
    category_dict.extractNew('receipts_test.csv')
    assert '' not in category_dict.item_category_dict
    assert 'Bio Company' not in category_dict.item_category_dict
    assert category_dict.item_category_dict['Blanc de Pomm'] == 'Zubrot';



