# -*- coding: utf-8 -*-
from pyramid.view import view_config
from receipteval.storage.sqlite import sqlite
from receipteval.receipt_collection import ReceiptCollection
import pprint


@view_config(route_name='statistics_route')
def statistics_view(request):
    db = sqlite()
    purchases = db.getPurchasesByTimespan("2016-01-01", "2016-12-31")
    collection = ReceiptCollection(purchases)
    collection.collect_items()
    html =  "<h1>total: " + str(collection.total) + "</h1><ul>"
    for category, value in collection.categories.items():
        html += "<li>" + category + " " + str(value[0]) + "</li>"
    html += "</ul>"
    return {'form': html}

