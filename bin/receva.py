#!/usr/bin/env python 
# encoding: utf-8
import argparse
from receipteval.parser import parser as recevap

script_description = ('Evaluate receipts stored as .csv')
parser = argparse.ArgumentParser(description=script_description)
parser.add_argument("receipts_file", help="path to the .csv file with " + 
                    "the data from the receipts")
#parser.add_argument("-v", "--verbose", action="store_true",
#                    help="increase output verbosity")
#parser.add_argument("-l", "--log-file",
#                    help="if specified, create full log at given location")
parser.add_argument("-c", "--categories", action="store_true",
                    help="show all categories")
parser.add_argument("--show-category",
                    help="show all items in a category", metavar=('CATEGORY'))
parser.add_argument("--show-null", action="store_true",
                    help='Show items without category')
parser.add_argument("-s","--check-sanity", action="store_true",
                    help='Check if an item belongs to two or more categories')

args = parser.parse_args()

with recevap() as p:
    rc = p.readFile(args.receipts_file)
rc.collectItems()
for key in rc.categories:
    print 'Category ' + key + ': ' + str(rc.categories[key][0])




if __name__ == "__main__":
    pass
