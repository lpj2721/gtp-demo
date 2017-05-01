#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib
import conf
# from lib_util import randomStr
from db_conn.cont_redis import g_session_redis
from wx_cgibase import cgibase
from wx_opr.basic_info import basic_info as db



class Clogin(cgibase):
    def __init__(self):
        self.oprlist = {
            "login":self.login,
            "check":self.check_info
        }
        return cgibase.__init__(self)

    def onInit(self):
        cgibase.SetNoCheckCookie(self)
        opr = cgibase.onInit(self)
        if opr is None:
            return
        if opr not in self.oprlist :
            return
        self.oprlist[opr]()

    def login(self):
        self.log.debug("join in.")
        req = self.input["input"]
        code = req["code"]


    def check_info(self):
        if not self.checkCookie():
            return None
        self.log.debug('check_info')
        req = self.input["input"]
        rawData = req['data']['rawData']
        signature = req['data']['signature']
        sid = self.input["self"]["ssid"]
        value = g_session_redis.get(conf.g_redis_pix + sid)
        session_key = value.split(conf.ssid_pix)[1]
        sign_data = rawData + session_key
        check_signature = hashlib.sha1(sign_data).hexdigest()
        if signature == check_signature:
            self.out = '{"status":0,"msg":"验签成功！"}'
            return self.out
        else:
            self.out = '{"status":1,"msg":"验签失败！"}'
            return self.out

if __name__ == "__main__":
    login = Clogin()
    login.onInit()
