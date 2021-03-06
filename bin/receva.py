#!/usr/bin/env python
# encoding: utf-8
import argparse
from receipteval.parser import Parser as ReceiptParser
from receipteval.item_cat_dict import ItemCategoryDict
from receipteval.helper import simplify_category
from receipteval.receipt_collection import ReceiptCollection

script_description = ('Evaluate receipts stored as .csv')
parser = argparse.ArgumentParser(description=script_description)
parser.add_argument("receipts_file", help="path to the .csv file with " +
                    "the data from the receipts")
parser.add_argument("-c", "--categories-file",
                    help="specify which category file to use", metavar=('CATEGORYFILE'))
parser.add_argument("--categories", action="store_true",
                    help="show all categories")
parser.add_argument("--show-category",
                    help="show all items in a category", metavar=('CATEGORY'))
parser.add_argument("-0", "--show-null", action="store_true",
                    help='Show items without a category')
parser.add_argument("-s", "--check-sanity", action="store_true",
                    help='Check if an item belongs to two or more categories\n' +
                    'Does not count the "empty category"')
parser.add_argument("-S", "--check-categories", action="store_true",
                    help='Check Categories')
parser.add_argument("-u", "--update-categories", action="store_true",
                    help='Update the categories file')
parser.add_argument("-l", "--ledger", action="store_true",
                    help="show receipts in ledger format ")
parser.add_argument("-d", "--date", metavar=('date'), default="1900-01-01",
                    help="show only output from this day on")

args = parser.parse_args()

parser_args = {}

if args.categories_file:
    cat_dict = ItemCategoryDict(path=args.categories_file)
    parser_args['category_dictionary'] = cat_dict

with ReceiptParser(**parser_args) as p:
    purchases = p.read_file(args.receipts_file)
rc = ReceiptCollection(purchases)
rc.collect_items()

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
    print "The following items are in more than one category or their price is missing:"
    for item in rc.unsane_items:
        print item
elif args.check_categories:
    for (item, inputCategory, storedCategory) in rc.unsane_categories:
        print item + " " + inputCategory + " " + storedCategory
elif args.update_categories:
    rc.category_dict.update_cat_file(args.receipts_file, args.categories_file)
elif args.ledger:
    ledger = rc.get_ledger(args.date)
    print ledger
else:
    for key in rc.categories:
        if key == 'Category':
            continue
        simpleKey = simplify_category(key)
        catTotal = rc.categories[key][0]
        print "{0:6.2f}".format(catTotal) + ' ' + "{0:4.1f}".format(catTotal/rc.total*100.0) + "% " + simpleKey + " ({0:d})".format(len(rc.categories[key][1]))
    print "{0:6.2f}".format(rc.total) + "       " + "Total"


if __name__ == "__main__":
    pass
