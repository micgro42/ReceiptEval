# encoding: utf-8

from receipteval.helper import simplify_category
from receipteval.helper import validate_date
from datetime import datetime


def test_simplify_category_noColon():
    test_category = 'b'

    result = simplify_category(test_category)

    assert result == 'b'


def test_simplify_category_oneColon():
    test_category = 'a:b'

    result = simplify_category(test_category)

    assert result == 'b'


def test_simplify_category_twoColon():
    test_category = 'a:b:c'

    result = simplify_category(test_category)

    assert result == 'c'


#def test_validate_date_consecutive():
    '''TODO: must raise exception'''
#    test_date = '20150914'

#    result = validate_date(test_date)


def test_validate_date_iso():
    test_date = '2015-09-14'

    result = validate_date(test_date)

    assert result == datetime(2015, 9, 14, 0, 0)


def test_validate_date_old_format():
    '''TODO: must raise warning'''
    test_date = '14.09.15'

    result = validate_date(test_date)

    assert result == datetime(2015, 9, 14, 0, 0)