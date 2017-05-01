#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2017-02-21 9:38
@author: LZJ
"""

from db_conn.cont_mongo import MongoConn

db = MongoConn().conn["QTP"]
a = {"_id":"199312","count":1}
db['test'].insert_one(a)

b = db['test'].find_one("199312")
print(b)