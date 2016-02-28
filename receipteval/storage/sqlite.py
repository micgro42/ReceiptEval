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
                       "pk_receipt_id INTEGER PRIMARY KEY," +
                       "date date," +
                       "shop text," +
                       "flags text," +  # comma separated, suboptimal
                       "fk_category_id text" +
                       " )")
                c.execute(sql)
                self.conn.commit()

            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = ?", ('categories',))
            if c.fetchone() is None:
                sql = ("CREATE TABLE categories ( " +
                       "name text PRIMARY KEY NOT NULL," +
                       "comment text" +
                       " )")
                c.execute(sql)
                self.conn.commit()

            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = ?", ('items',))
            if c.fetchone() is None:
                sql = ("CREATE TABLE items ( " +
                       "pk_item_id INTEGER PRIMARY KEY," +
                       "name text," +
                       "EAN int," +
                       "comment text" +
                       " )")
                c.execute(sql)
                self.conn.commit()

            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = ?", ('positions',))
            if c.fetchone() is None:
                sql = ("CREATE TABLE positions ( " +
                       "fk_receipt_id INTEGER," +
                       "fk_item_id INTEGER," +
                       "fk_category_id text," +
                       "price money," +
                       "quantity int," +
                       "tags text" +
                       " )")
                c.execute(sql)
                self.conn.commit()

        except sqlite3.Error as e:
            print ("Error %s:" % e.args[0])
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
        purchaseID = c.lastrowid
        # If I replace an new purchase into the database - how do I get its ID?
        ok = True
        for position in positions:
            ok = ok and self.addPosition(position)

    def getPurchases(self):
        NotImplementedError("Class %s doesn't implement getPurchases()"
                            % (self.__class__.__name__))

    def addItem(self, entity):
        sql = 'REPLACE INTO items (name, EAN, comment) VALUES (?, ?, ?)'
        c = self.conn.cursor()
        t = (entity['name'], entity['ean'], entity['comment'])
        try:
            c.execute(sql, t)
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
            self.conn.rollback()
            return False
        return True

    def addCategory(self, entity):
        sql = 'REPLACE INTO categories (name, comment) VALUES (?, ?)'
        c = self.conn.cursor()
        t = (entity['name'], entity['comment'])
        try:
            c.execute(sql, t)
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
            self.conn.rollback()
            return False
        return True

    def getCategory(self, name):
        c = self.conn.cursor()
        sql = "SELECT * FROM categories WHERE name = ?"
        c.execute(sql, name)
        return c.fetchone()

    def getAllCategories(self):
        c = self.conn.cursor()
        sql = "SELECT * FROM categories"
        c.execute(sql)
        return c.fetchall()

    def getAllItems(self):
        c = self.conn.cursor()
        sql = "SELECT * FROM items"
        c.execute(sql)
        return c.fetchall()


    def addPosition(self, position):
        NotImplementedError("Class %s doesn't implement getPurchases()"
                            % (self.__class__.__name__))


    """
    /**
     * Saves the given key-value array to the given table
     *
     * @param string table
     * @param dict entity associative array holding the key/value pairs
     */
     """
    def saveEntity(self, table, entity):
        c = self.conn.cursor()

        keys = ', '.join(entity.keys());
        vals = entity.values()
        wlds = ', '.join('?'*len(vals));

        sql = 'REPLACE INTO '+table+' ('+keys+') VALUES ('+wlds+')'
        try:
            c.execute(sql, vals)
            self.conn.commit()
        except Error(e):
            print(e)
            self.conn.rollback()
            return false
        return true




























if __name__ == "__main__":
    s = sqlite()