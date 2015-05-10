# -*- coding: utf-8 -*-
'''
Created on May 10, 2015

@author: Michael Große <mic.grosse@posteo.de>
'''

from collections import namedtuple

class purchase(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        self.date = params['date']
        self.shop = params['shop']
        self.positions = [namedtuple('item', ['name','count','category','ppi','weight'])]
        self.total = 0.0