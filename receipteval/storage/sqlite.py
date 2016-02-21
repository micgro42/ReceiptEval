#!/usr/bin/env python
# encoding: utf-8
from storage import IStorage
import sqlite3
import sys


class sqlite(IStorage):
    '''
    classdocs
    '''

    def __init__(self, dbpath='db.sqlite'):
        try:
            conn = sqlite3.connect(dbpath)
            c = conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = ?", ('receipts',))
            if c.fetchone() is None:
                sql = ("CREATE TABLE receipts ( " +
                       "pk_receipt_id int PRIMARY KEY," +
                       "date date," +
                       "shop text," +
                       "fk_category_id int" +
                       " )")
                c.execute(sql)
                c.commit()
            else:
                c.execute("PRAGMA table_info('receipts')")
                print c.fetchall()

            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = ?", ('categories',))
            if c.fetchone() is None:
                sql = ("CREATE TABLE categories ( " +
                       "pk_category_id int PRIMARY KEY," +
                       "name text," +
                       "comment text" +
                       " )")
                c.execute(sql)
                conn.commit()
            else:
                c.execute("PRAGMA table_info('categories')")
                print c.fetchall()

            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = ?", ('items',))
            if c.fetchone() is None:
                sql = ("CREATE TABLE items ( " +
                       "pk_item_id int PRIMARY KEY," +
                       "name text," +
                       "comment text" +
                       " )")
                c.execute(sql)
                conn.commit()
            else:
                c.execute("PRAGMA table_info('items')")
                print c.fetchall()

            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = ?", ('positions',))
            if c.fetchone() is None:
                sql = ("CREATE TABLE positions ( " +
                       "fk_receipt_id int," +
                       "fk_item_id int," +
                       "fk_category_id int," +
                       "price money,"
                       "quantity int," +
                       "EAN int," +
                       "tags text" +
                       " )")
                c.execute(sql)
                conn.commit()
            else:
                c.execute("PRAGMA table_info('positions')")
                print c.fetchall()

        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

    def addPurchase(self, purchase):
        NotImplementedError("Class %s doesn't implement addPurchase()"
                            % (self.__class__.__name__))

    def getPurchases(self):
        NotImplementedError("Class %s doesn't implement getPurchases()"
                            % (self.__class__.__name__))




if __name__ == "__main__":
    s = sqlite()