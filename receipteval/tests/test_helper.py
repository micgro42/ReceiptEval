# encoding: utf-8

from receipteval.helper import simplify_category


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
