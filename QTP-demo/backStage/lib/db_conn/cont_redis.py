#!/usr/bin/env python
#coding=utf-8

from db_conf import W_Redis_CONFIG,S_Redis_CONFIG
import redis

s_pool = redis.ConnectionPool(host=S_Redis_CONFIG["ip"], port=S_Redis_CONFIG["port"], db=0)
g_session_redis = redis.Redis(connection_pool=s_pool)

