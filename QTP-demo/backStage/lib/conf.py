#!/usr/bin/python
# -*- coding: utf-8 -*-

debug_mode = True #False
url_pre = "/"
g_redis_pix = "wx_"
ord_pix ="ord_"
p_redis_pix = "paw_"
ssid_pix = "_wx_"
g_ssid_timeout = 3600*24
ord_timeout = 60*15
sms_timeout = 15*60
pay_pwd_lock= 2*60*60
pay_recount = 24*60*60
cgi_log_path = "/data/C_cgi/"
max_cgilog_size = 70 * 1024 * 1024
session_redis = {"ip" :"123.206.109.249", "port" :6379} #会话redis


rSyslog = ('127.0.0.1',514)
err = {
    "refused":'{"status":1, "msg":"拒绝访问！"}',
    "input_err":'{"status":2, "msg":"输入错误！"}',
    "relogin":'{"status":3, "msg":"会话超时，需要重新登录！", "need_login":1}',
    "ext_error":'{"status":4, "msg":"上传文件的扩展名不支持。"}',
    "wx_err": '{"status":10001,"msg": "系统维护中！请稍后尝试该操作"}'
}

