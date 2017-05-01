#!/usr/bin/env python
# coding=utf-8
# import commands
import json
import logging
import logging.handlers
import sys
from imp import reload
from urllib.parse import unquote,urlparse
import conf
from db_conn.cont_redis import g_session_redis


class cgibase:
    def __init__(self):
        self.myinit()

    def __del__(self):
        self.mydel()

    def myinit(self):
        self.out = {}
        self.input = {}
        self.out_ssid = None
        self.redirect_url = None
        self.log_handler = None
        self.__cookieFlag = True
        self.name = None
        self.log = None
        self.isdebug = False

    def mydel(self):
        if self.log_handler is not None:
            self.log.removeHandler(self.log_handler)
            self.log_handler = None
        if self.isdebug is True:
            print(self.output())

    def setenv(self, req_dict):
        self.input = req_dict

    def output(self):
        if type(self.out) is dict:
            self.out = json.dumps(self.out, ensure_ascii=False)
        self.log.debug("cgibase out is %s..." % self.out)
        return self.out

    def onInit(self):
        reload(sys)
        if self.input == {}:
            self.isdebug = True
            self.SetNoCheckCookie()
            if len(sys.argv) != 3:
                self.out = conf.err["input_err"]
                return None
            self.input["self"] = {}
            self.input["self"]["fun"] = sys.argv[1]
            self.input["self"]["ip"] = "127.0.0.1"
            self.input["self"]["ssid"] = None
            self.input["self"]["m"] = "GET"
            arg = sys.argv[2]
            isjson = False
            if arg.find("file://") == 0:
                self.input["self"]["m"] = "POST"
                try:
                    file = open(arg[len("file://"):])
                except:
                    self.out = conf.err["input_err"]
                    return None
                else:
                    data_in = file.read()
                    file.close()
                    try:
                        json.loads(data_in)
                    except:
                        isjson = False
                    else:
                        isjson = True
            else:
                data_in = arg
            jsondata = {}
            if isjson is False:
                data_in = unquote(data_in)
                data_in = urlparse(data_in)
                for dat in data_in:
                    jsondata[dat[0]] = dat[1]
            else:
                jsondata = json.loads(data_in)
            self.input["input"] = jsondata

        cginame = self.input["self"]["fun"]
        handler = logging.handlers.SysLogHandler(address=conf.rSyslog, facility="local4")
        fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        self.log = logging.getLogger(cginame)
        self.log_handler = handler
        self.log.addHandler(handler)
        self.log.setLevel(logging.DEBUG)

        self.log.debug('\n\n### start debug log ###\n')
        self.log.debug(json.dumps(self.input, ensure_ascii=False))

        if self.__cookieFlag:
            if not self.checkCookie():
                return None

        opr = None
        if not self.input["input"].has_key("opr"):
            self.out = conf.err["input_err"]
            return opr
        opr = self.input["input"]["opr"]

        return opr

    def SetNoCheckCookie(self):
        self.__cookieFlag = False
        return

    def checkCookie(self):
        sid = self.input["self"]["ssid"]
        if (sid == '' or sid is None):
            self.out = conf.err["relogin"]
            return False  # cookie error
        r = g_session_redis.get(conf.g_redis_pix + sid)
        if r is None or r == "":
            self.out = conf.err["relogin"]
            return False  # cookie error
        self.name = r
        check_sid = g_session_redis.get(r)
        if conf.g_redis_pix + sid == check_sid:
            g_session_redis.expire(conf.g_redis_pix + sid, conf.g_ssid_timeout)
            return True
        else:
            g_session_redis.delete(conf.g_redis_pix + sid)
            self.out = conf.err["relogin"]
            return False


if __name__ == "__main__":
    pass
