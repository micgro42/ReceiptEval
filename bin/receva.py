#!/usr/bin/env python 
# encoding: utf-8
import argparse
from receipteval.parser import parser as recevap

script_description = ('Evaluate receipts stored as .csv')
parser = argparse.ArgumentParser(description=script_description)
parser.add_argument("receipts_file", help="path to the .csv file with " + 
                    "the data from the receipts")
parser.add_argument("-c", "--categories", action="store_true",
                    help="show all categories")
parser.add_argument("--show-category",
                    help="show all items in a category", metavar=('CATEGORY'))
parser.add_argument("-0","--show-null", action="store_true",
                    help='Show items without a category')
parser.add_argument("-s","--check-sanity", action="store_true",
                    help='Check if an item belongs to two or more categories\n'+
                    'Does not count the "empty category"')

args = parser.parse_args()

with recevap() as p:
    rc = p.readFile(args.receipts_file)

rc.collectItems()

if args.categories:
    for key in rc.categories:
        print key
elif args.show_null:
    print 'Items without category:'
    for item in rc.categories[''][1]:
        print item
elif args.show_category is not None:
    print 'Items in category ' + args.show_category + ':'
    for item in rc.categories[args.show_category][1]:
        print item
elif args.check_sanity:
    print "The following items are in more than one category:"
    for item in rc.unsane_items:
        print item
else:
    for key in rc.categories:
        if key == 'Category':
            continue
        if rc.categories[key][0] >= 100.00:
            prespace = ''
        elif rc.categories[key][0] >= 10.00:
            prespace = ' '
        elif rc.categories[key][0] >= 0.0:
            prespace = '  '
        else:
            prespace = ' '

        print "{0:6.2f}".format(rc.categories[key][0]) + ' ' + key




if __name__ == "__main__":
    pass
