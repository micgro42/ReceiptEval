# encoding: utf-8

from receipteval.purchase import Purchase
from collections import namedtuple
from receipteval.item_cat_dict import ItemCategoryDict


def test_purchase():
    expected_positions = []
    cat_dict = ItemCategoryDict()
    cat_dict.item_category_dict = {'Pfand': 'Pfand', 'Cola Zero': 'Cola'}
    Position = namedtuple('item', ['name',
                                   'category',
                                   'price',
                                   'count',
                                   'weight'])
    expected_positions.append(Position('Cola Zero', 'Cola', 0.39, 1, '1.5l'))
    expected_positions.append(Position('Pfand', 'Pfand', 0.25, 1, ''))
    expected_positions.append(Position('Mandelhörnchen', '', 1.59, 1, ''))
    expected_positions.append(Position('Kaffeegetränk', '', 0.49, 1, '0.25l'))
    expected_positions.append(Position('Schokolade Edelbitter',
                                       '',
                                       1.09,
                                       1,
                                       ''))
    expected_positions.append(Position('Schokolade Erdbeere Joghurt Crisp',
                                       '',
                                       1.19,
                                       1,
                                       '200g'))
    with Purchase('2015-05-21',
                  'Aldi',
                  payment_method='cash',
                  category_dict=cat_dict) as purchase:
        purchase.addItem('Cola Zero', 0.39, 1, weight='1.5l')
        purchase.addItem('Pfand', 0.25, 1)
        purchase.addItem('Mandelhörnchen', 1.59, 1)
        purchase.addItem('Kaffeegetränk', 0.49, 1, weight='0.25l')
        purchase.addItem('Schokolade Edelbitter', 1.09, 1)
        purchase.addItem('Schokolade Erdbeere Joghurt Crisp',
                         1.19,
                         1,
                         weight='200g')
        assert expected_positions == purchase.positions
        assert purchase.total == 5


def test_purchase_ledger():
    cat_dict = ItemCategoryDict()
    cat_dict.item_category_dict = {'Pfand': 'Aktiva:Pfand',
                                   'Cola': 'Ausgaben:Konsum:Cola'}
    with Purchase('2015-05-21',
                  'Testgeschäft',
                  payment_method='cash',
                  category_dict=cat_dict) as purchase:
        purchase.addItem('Cola', 0.39, 1, weight='1.5l')
        purchase.addItem('Pfand', 0.25, 1)
    actual_output = purchase.getLedger()
    expected_output = "2015-05-21 Testgeschäft\n"
    expected_output += "  Aktiva:Portmonaie  -0.64\n"
    expected_output += "  Ausgaben:Konsum:Cola  0.39\n"
    expected_output += "  Aktiva:Pfand  0.25\n"
    expected_output += "\n"
    assert expected_output == actual_output


def test_purchase_ledger_only():
    cat_dict = ItemCategoryDict()
    cat_dict.item_category_dict = {'Pfand': 'Aktiva:Pfand',
                                   'Cola': 'Ausgaben:Konsum:Cola'}
    with Purchase('2015-05-21',
                  'Übertrag',
                  payment_method='Giro',
                  category_dict=cat_dict,
                  flags='L') as purchase:
        purchase.addItem('Auszahlung', 100, 1, category='Aktiva:Portmonaie')
    actual_output = purchase.getLedger()
    expected_output = "2015-05-21 Übertrag\n"
    expected_output += "  Aktiva:Giro  -100.0\n"
    expected_output += "  Aktiva:Portmonaie  100.0\n"
    expected_output += "\n"
    assert expected_output == actual_output
