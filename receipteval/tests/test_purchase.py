# encoding: utf-8


import pytest
from receipteval.purchase import Purchase
from collections import namedtuple


def test_purchase():
    expected_positions = []
    Position = namedtuple('item', ['name','category','price','count','weight'])
    with Purchase('2015-05-21','Aldi',payment_method = 'cash') as purchase:
        purchase.addItem('Cola Zero',0.39,1)
        expected_positions.append(Position('Cola Zero','',0.39,1,''))
        purchase.addItem('Pfand',0.25,1)
        expected_positions.append(Position('Pfand','',0.25,1,''))
        purchase.addItem('Mandelhörnchen',1.59,1)
        expected_positions.append(Position('Mandelhörnchen','',1.59,1,''))
        purchase.addItem('Kaffeegetränk',0.49,1)
        expected_positions.append(Position('Kaffeegetränk','',0.49,1,''))
        purchase.addItem('Schokolade Edelbitter',1.09,1)
        expected_positions.append(Position('Schokolade Edelbitter','',1.09,1,''))
        purchase.addItem('Schokolade Erdbeere Joghurt Crisp',1.19,1)
        expected_positions.append(Position('Schokolade Erdbeere Joghurt Crisp','',1.19,1,''))
        assert purchase.positions == expected_positions
        assert purchase.total==5
    
