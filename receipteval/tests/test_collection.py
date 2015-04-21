# encoding: utf-8
'''
Created on Apr 19, 2015

@author: Michael Große <mic.grosse@posteo.de>
'''

import pytest

from receipteval.receiptCollection import receiptCollection

def test_category_correct():
    rC = receiptCollection()
    rC.checkCategory('Milch','Heumilch')
    assert not rC.unsane_categories

def test_category_wrong():
    rC = receiptCollection()
    rC.checkCategory('Obst','Heumilch')
    assert rC.unsane_categories[0] == ('Heumilch', 'Obst', 'Milch')
    
def test_category_missing():
    rC = receiptCollection()
    rC.checkCategory('','Heumilch')
    assert rC.unsane_categories[0] == ('Heumilch', '', 'Milch')

def test_category_stored_missing():
    rC = receiptCollection()
    rC.checkCategory('Testcategory','Testitem')
    assert rC.unsane_categories[0] == ('Testitem', 'Testcategory', '')
    
def test_category_both_missing():
    rC = receiptCollection()
    rC.checkCategory('','Testitem')
    assert not rC.unsane_categories