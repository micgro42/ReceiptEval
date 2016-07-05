# -*- coding: utf-8 -*-
from pyramid.view import view_config
from receipteval.storage.sqlite import sqlite
from receipteval.receipt_collection import ReceiptCollection
import pprint
import datetime


def collectByTimespan(start, end):
    # print(start + " " + end)
    db = sqlite()
    purchases = db.getPurchasesByTimespan(start, end)
    collection = ReceiptCollection(purchases)
    collection.collect_items()
    collection.totalize_categories()
    return collection


def getWeeks(year):
    # get first week
    jan1 = datetime.date(year, 1, 1)
    firstday = jan1 - datetime.timedelta(jan1.isocalendar()[2]-1)
    if (jan1.isocalendar()[1] != 1):
        firstday += datetime.timedelta(7)
    collections = {}
    while (firstday.isocalendar()[0] == year):
        lastday = firstday + datetime.timedelta(6)
        collections[firstday.isocalendar()[1]] = collectByTimespan(firstday.isoformat(), lastday.isoformat())
        # pprint.pprint(collections[firstday.isocalendar()[1]].categories)
        firstday = lastday + datetime.timedelta(1)
    return collections


@view_config(route_name='statistics_route')
def statistics_view(request):
    weeks_collect = getWeeks(2016)
    # pprint.pprint(weeks_collect)
    collection = collectByTimespan("2016-01-01", "2016-12-31")
    html = "<h1>total: " + str(round(collection.total, 2)) + "</h1><ul>"
    for category, value in collection.categories.items():
        html += "<li>" + category + " " + str(round(value[0], 2)) + "</li>"
    html += "</ul>"
    html += "<h2>weeks</h2><ul>"
    for week, collect in weeks_collect.items():
        html += "<li>" + str(week) + " Ausgaben: " + str(round(collect.categories['Ausgaben'][2], 2)) + "</li>"
        html += "<li>" + str(week) + " Konsum: " + str(round(collect.categories['Ausgaben:Konsum'][2], 2)) + "</li>" 
    html += "</ul>"
    return {'form': html}

