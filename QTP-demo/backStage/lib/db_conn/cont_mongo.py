#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2016-12-02 9:44
@author: LZJ
"""
import pymongo
import sys
from db_conf import MONGODB_CONFIG


class MongoConn():

    def __init__(self):
        # connect db

        self.conn = pymongo.MongoClient(MONGODB_CONFIG['host'], MONGODB_CONFIG['port'])
        self.db = self.conn[MONGODB_CONFIG['db_name']]  # connect db
        self.username = MONGODB_CONFIG['username']
        self.password = MONGODB_CONFIG['password']
        if self.username and self.password:
            self.connected = self.db.authenticate(self.username, self.password)
        else:
            self.connected = True

    pass

pass
