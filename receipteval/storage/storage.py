'''
Created on Dec 5, 2015

@author: michael
'''
from abc import ABCMeta, abstractmethod


class IStorage:
    '''
    classdocs
    '''

    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def addPurchase(self, purchase):
        NotImplementedError("Class %s doesn't implement addPurchase()"
                            % (self.__class__.__name__))

    @abstractmethod
    def getPurchases(self):
        NotImplementedError("Class %s doesn't implement getPurchases()"
                            % (self.__class__.__name__))
