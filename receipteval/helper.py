'''
Created on May 25, 2015

@author: michael
'''


from datetime import datetime
from datetime import date
from _warnings import warn


def validate(date_text):
    '''
    validate that the parameter is actually a date string and return the date
    throw an exception otherwise
    :param date_text:
    '''
    if isinstance(date_text, date):
        return date_text
    try:
        valid_date = datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        try:
            valid_date = datetime.strptime(date_text, '%d.%m.%y')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD" +
                             " but is " + date_text)
        else:
            warn('The date format is ambiguous and should be avoided: ' +
                 date_text, RuntimeWarning)
    return valid_date


def simplify_category(category):
    '''
    return only the last part of an account/category
    :param category: the categpry to be simplyfied
    :type category: string
    '''
    colon_position = category.rfind(":")
    if colon_position is not -1:
        category = category[colon_position+1:]
    return category
