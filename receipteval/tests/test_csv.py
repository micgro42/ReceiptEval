# -*- coding: utf-8 -*-
'''
Created on Apr 19, 2015

@author: Michael Große <mic.grosse@posteo.de>
'''

import unittest
import csv


class TestCSV(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_csv_write(tmpdir):
        with open('testfile.csv', 'wb') as testfile:
            csv_writer = csv.writer(testfile, lineterminator='\n')
            csv_writer.writerow(["foo", "bar"])
            csv_writer.writerow(["baz", "foobar"])
        with open('testfile.csv', 'r') as testfile:
            assert testfile.read() == 'foo,bar\nbaz,foobar\n'

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
