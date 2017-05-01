#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request, make_response, redirect
import json,os,sys,time
import conf

from login import Clogin

app = Flask(__name__)
app.debug = conf.debug_mode


def pre_do(c, fun, ext_type=None):
    req_dict = {}
    if request.method == "GET":
        req_dict = request.values
        print(req_dict.get('_page'))
    elif request.method == "POST":
        if ext_type=="file_up":
            req_dict["input"] = {"opr": "upload"}
        elif ext_type=="wx_notify":
            req_dict["input"] = dict(opr="update", data=request.get_data())
            pass
        else:
            try:
                req_dict["input"] = json.loads(request.get_data())
                print(req_dict)
            except:

                return conf.err["refused"]
    elif request.method == "PATCH":
        req_dict["input"] = json.loads(request.get_data())
        print(req_dict)
        return json.dumps(req_dict)
    ip = request.headers.get('X-Real-IP')
    if ip is None or ip == "":
        ip = "127.0.0.1"
    ssid = request.headers.get('ssid')
    if ssid is None:
        ssid = ''
    req_dict["self"] = {}
    req_dict["self"]["ip"] = ip
    req_dict["self"]["ssid"] = ssid
    req_dict["self"]["m"] = request.method
    req_dict["self"]["fun"] = fun

    c.setenv(req_dict)
    try:
        c.myinit()
        c.setenv(req_dict)
        c.onInit()
    except:
        c.mydel()
        raise
    out = c.output()
    redirect_url = c.redirect_url
    c.mydel()

    if redirect_url is not None:
        return redirect(redirect_url)
    resp = make_response(out)
    return resp


@app.route(conf.url_pre + "users", methods = ['GET', 'POST', 'PATCH'])
def login_func():
    return pre_do(Clogin(),"login")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)