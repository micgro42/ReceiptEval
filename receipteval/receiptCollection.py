'''
Created on Nov 30, 2014

@author: michael
'''

class receiptCollection(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.categories = {}
        self.receipt_lines = []
        self.unsane_items = []

    def collectItems(self):
        for line in self.receipt_lines:
            date = line[0]
            item = line[2]
            category = line[4]
            if (date is '' and
                item is not ''):
                try:
                    price = float(line[3])
                except ValueError:
                    print 'incorrect price "' + line[3] + '"'
                    raise
                self.categories[category][1].add(item)
                self.categories[category][0] += price
        self.checkSanity()

    def checkSanity(self):
        all_items = set()
        for c in self.categories:
            if c is '':
                continue
            for item in self.categories[c][1]:
                if item in all_items:
                    self.unsane_items.append(item)
                all_items.add(item)
