'''
Created on Nov 30, 2014

@author: michael
'''
import csv
from receipteval.receiptCollection import receiptCollection

class parser(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        print 'parser init'
        self.receipt_lines = []

    def __enter__(self):
        print 'parser enter'
        return self

    def __exit__(self, thetype, value, traceback):
        print 'parser exit'
        #return True # todo: is this line necessary? 

    def readFile(self, file_path):
        with open(file_path, 'rb') as receipt_file:
            csv_reader = csv.reader(receipt_file)
            for line in csv_reader:
                self.receipt_lines.append(line)

        rc = receiptCollection()
        for i,line in enumerate(self.receipt_lines):
            if line[4] not in rc.categories:
                rc.categories[line[4]] = [0.0,set()]

        # /todo: add cleanup, remove empty lines, etc. #todo TODO
        rc.receipt_lines = self.receipt_lines
        return rc
