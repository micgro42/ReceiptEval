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
            self.conn = sqlite3.connect(dbpath)
            c = self.conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = ?", ('receipts',))
            if c.fetchone() is None:
                sql = ("CREATE TABLE receipts ( " +
                       "pk_receipt_id int PRIMARY KEY," +
                       "date date," +
                       "shop text," +
                       "flags text," +  # comma separated, suboptimal
                       "fk_category_id text" +
                       " )")
                c.execute(sql)
                c.commit()
            else:
                c.execute("PRAGMA table_info('receipts')")
                print c.fetchall()

            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = ?", ('categories',))
            if c.fetchone() is None:
                sql = ("CREATE TABLE categories ( " +
                       "name text PRIMARY KEY," +
                       "comment text" +
                       " )")
                c.execute(sql)
                self.conn.commit()
            else:
                c.execute("PRAGMA table_info('categories')")
                print c.fetchall()

            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = ?", ('items',))
            if c.fetchone() is None:
                sql = ("CREATE TABLE items ( " +
                       "pk_item_id int PRIMARY KEY," +
                       "name text," +
                       "EAN int," +
                       "comment text" +
                       " )")
                c.execute(sql)
                self.conn.commit()
            else:
                c.execute("PRAGMA table_info('items')")
                print c.fetchall()

            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = ?", ('positions',))
            if c.fetchone() is None:
                sql = ("CREATE TABLE positions ( " +
                       "fk_receipt_id int," +
                       "fk_item_id int," +
                       "fk_category_id text," +
                       "price money," +
                       "quantity int," +
                       "tags text" +
                       " )")
                c.execute(sql)
                self.conn.commit()
            else:
                c.execute("PRAGMA table_info('positions')")
                print c.fetchall()

        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

    def addPurchase(self, purchase):
        if self.getCategory(purchase.payment_method) is None:
            return False
        category = purchase.payment_method
        flags = purchase.flags
        date = purchase.date
        shop = purchase.shop
        positions = purchase._positions # todo: we need the positions even if this is a ledger transaction!
        sql = ("REPLACE INTO receipts (" +
               "date, shop, flags, fk_category_id ) VALUES (?, ?, ?, ?)")
        c = self.conn.cursor()
        t = (date, shop, flags, category)
        c.execute(sql, t)
        # If I replace an new purchase into the database - how do I get its ID?
        ok = True
        for position in positions:
            ok = ok && self.addPosition(position)

    def getPurchases(self):
        NotImplementedError("Class %s doesn't implement getPurchases()"
                            % (self.__class__.__name__))

    def addItem(self, item):
        NotImplementedError("Class %s doesn't implement getPurchases()"
                            % (self.__class__.__name__))

    def addCategory(self, category):
        NotImplementedError("Class %s doesn't implement getPurchases()"
                            % (self.__class__.__name__))

    def getCategory(self, name):
        c = self.conn.cursor()
        sql = "SELECT * FROM categories WHERE name = ?"
        c.execute(sql, name)
        return c.fetchone()

    def getAllCategories(self):
        sql = "SELECT * FROM categories"
        NotImplementedError("Class %s doesn't implement getPurchases()"
                            % (self.__class__.__name__))

    def addPosition(self, position):
        NotImplementedError("Class %s doesn't implement getPurchases()"
                            % (self.__class__.__name__))































if __name__ == "__main__":
    s = sqlite()