# -*- coding: utf-8 -*-
"""
provide class item_category_dict
"""
class ItemCategoryDict(object):
    """
    Set the category for every item

    """
    item_category_dict = {
            'Pfand': 'Pfand',
            'Pesto': 'Pesto',
            'Parmesan': 'Käse',
            'Heumilch': 'Milch',
            'Milch': 'Milch',
    }

    def __init__(self):
        pass

    def getCategory(self, item):
        """Return the category of an item

        :param item: name of item
        :type item: string
        """
        if item in self.item_category_dict:
            return self.item_category_dict[item]
        else:
            return ''
