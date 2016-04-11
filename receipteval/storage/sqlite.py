#!/usr/bin/env python
# encoding: utf-8

from receipteval.storage.storage import IStorage
from receipteval.purchase import Purchase
import sqlite3
import sys
from pprint import pprint


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
                       "pk_receipt_id INTEGER PRIMARY KEY AUTOINCREMENT," +
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
                       "fk_category_id text," +
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
                       "EAN int," +
                       "tags text" +
                       " )")
                c.execute(sql)
                self.conn.commit()

        except sqlite3.Error as e:
            print ("Error %s:" % e.args[0])
            sys.exit(1)

    def addPurchase(self, purchase):
        if self.getCategory((purchase['payment_method'],)) is None:
            return False
        category = purchase['payment_method']
        flags = purchase['flags']
        date = purchase['date']
        shop = purchase['shop']
        positions = purchase['positions'] # todo: we need the positions even if this is a ledger transaction!
        sql = ("INSERT INTO receipts (" +
               "date, shop, flags, fk_category_id ) VALUES (?, ?, ?, ?)")
        c = self.conn.cursor()
        values = (date, shop, ','.join(flags), category)
        try:
            c.execute(sql, values)
            purchaseID = c.lastrowid
            for position in positions:
                position['receipt_id'] = purchaseID
                self.addPosition(position)
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
            self.conn.rollback()
            return False
        return True

    def getPurchasesByTimespan(self, start, end):
        sql = ("SELECT * "
               "FROM receipts "
               "WHERE date >= ? AND date <= ? ")
        c = self.conn.cursor()
        parameters = (start, end)
        c.execute(sql, parameters)
        return self.createPurchaseObjects(c.fetchall())

    def createPurchaseObjects(self, metapurchases):
        purchases = []
        for meta in metapurchases:
            purchase = Purchase(meta[1],
                                meta[2],
                                payment_method=meta[4],
                                flags=meta[3])
            positions = self.getPositions(meta[0])
            for position in positions:
                purchase.add_item(name=position[1],
                                  count=position[0],
                                  category=position[2],
                                  price=position[3])
            purchases.append(purchase)
        return purchases

    def getPositions(self, receipt_id):
        sql = ("SELECT quantity, name, p.fk_category_id, price, EAN, tags "
               "FROM positions as p, items as i "
               "WHERE fk_receipt_id = ? AND p.fk_item_id = i.pk_item_id")
        c = self.conn.cursor()
        t = (receipt_id,)
        c.execute(sql, t)
        return c.fetchall()

    def getPurchases(self):
        NotImplementedError("Class %s doesn't implement getPurchases()"
                            % (self.__class__.__name__))

    def addItem(self, entity):
        sql = 'REPLACE INTO items (name, fk_category_id, comment) VALUES (?, ?, ?)'
        c = self.conn.cursor()
        t = (entity['name'], entity['category'], entity['comment'])
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
        sql = "SELECT * FROM categories ORDER BY name ASC"
        c.execute(sql)
        return c.fetchall()

    def getAllItems(self):
        c = self.conn.cursor()
        sql = "SELECT * FROM items ORDER BY name ASC"
        c.execute(sql)
        return c.fetchall()


    def addPosition(self, position):
        c = self.conn.cursor()
        sql = ("INSERT INTO positions " +
        "(fk_receipt_id, fk_item_id, fk_category_id, price, quantity, ean, tags) " +
        "VALUES (?, ?, ?, ?, ?, ?, ?)")
        values = (
                    position['receipt_id'],
                    position['item_id'],
                    position['category'],
                    position['price'],
                    position['quantity'],
                    position['ean'],
                    position['tags']
                  )
        c.execute(sql, values)

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
        except sqlite3.Error as e:
            print(e)
            self.conn.rollback()
            return False
        return True




























if __name__ == "__main__":
    s = sqlite()
