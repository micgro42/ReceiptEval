# encoding: utf-8
'''
Created on Dec 26, 2014

@author: Michael Große
'''
import pytest
import os
from receipteval.parser import parser


#class ParserTest():

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
                               ',2,Roggenmehl,3.98,Obst,,,,\n'])
    request.addfinalizer(teardown_factory_file)

def teardown_factory_file():
    if os.path.isfile("receipts_test.csv"):
        os.remove("receipts_test.csv")

def test_unsane_items(factory_file):
    pass 
