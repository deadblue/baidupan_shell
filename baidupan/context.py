# -*- coding: utf-8 -*-
'''
Created on 2014/07/06

@author: deadblue
'''

import logging
import os
import sys

from baidupan import util, config

_RWD = 'rwd'
_LWD = 'lwd'

# 上下文数据
_data = {}

def init(args):
    # 设置日志级别
    debug_mode = args.get('debug')
    log_file = file(os.path.join(os.getcwd(), 'debug.log'), 'w') if debug_mode else sys.stderr
    log_level = logging.DEBUG if debug_mode else logging.ERROR
    logging.basicConfig(level=log_level, stream=log_file,
                        format='%(asctime)s %(levelname)s %(name)s - %(message)s')
    # 初始化数据
    _data['alive'] = True
    _data[_RWD] = '/'
    # 本地工作目录
    lwd = args.get('local')
    if lwd and os.path.exists(lwd):
        lwd = os.path.abspath(lwd)
    else:
        lwd = config.get_localhome()
    if not lwd.endswith(os.sep):
        lwd += os.sep
    _data[_LWD] = lwd
    # cookie文件
    global cookie_file
    cookie_file = args.get('cookie')
    if cookie_file:
        cookie_file = os.path.abspath(cookie_file)
    else:
        cookie_file = util.get_data_file('.baidupan.cookie')
    # 初始化client
    import cookielib
    from baidupan import api, tree
    global cookie_jar, client
    cookie_jar = cookielib.MozillaCookieJar(cookie_file)
    if os.path.exists(cookie_file): cookie_jar.load()
    client = api.BaiduPanClient(cookie_jar, util.ascii_vcode_handler)
    # 初始化远程文件树
    global remote_tree
    remote_tree = tree.RemoteTree(client)

def put(name, value):
    global _data
    _data[name] = value
def get(name):
    global _data
    return _data.get(name)
def get_rwd():
    return get(_RWD)
def set_rwd(value):
    put(_RWD, value)
def get_lwd():
    return get(_LWD)
def set_lwd(value):
    put(_LWD, value)

def is_alive():
    return _data.get('alive')
def set_alive(alive):
    _data['alive'] = alive

# 定义常量
cookie_file = None
cookie_jar = None
client = None
remote_tree = None