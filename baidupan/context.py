# -*- coding: utf-8 -*-
'''
Created on 2014/07/06

@author: deadblue
'''

import logging
import os
import sys
from baidupan import util, config

_ALIVE = 'alive'
_RWD = 'rwd'
_LWD = 'lwd'

# 上下文数据
_data = {}

def init():
    # 解析运行参数
    args = util.parser_arguments(sys.argv[1:])
    # 设置日志级别
    global log_file
    log_file = open(os.path.join(os.getcwd(), 'debug.log'), 'w')
    log_level = logging.DEBUG if args.get('debug') else logging.ERROR
    logging.basicConfig(level=log_level, stream=log_file,
                        format='%(asctime)s %(levelname)s %(name)s - %(message)s')
    # 初始化数据
    _data[_RWD] = '/'
    _data[_LWD] = config.get_localhome()
    _data[_ALIVE] = True
    # 标记为活动
    # 初始化client
    import cookielib
    from baidupan import api, tree
    global cookie_file, cookie_jar, client, remote_tree
    cookie_file = util.get_data_file('.baidupan.cookie')
    cookie_jar = cookielib.MozillaCookieJar(cookie_file)
    if os.path.exists(cookie_file): cookie_jar.load()
    client = api.BaiduPanClient(cookie_jar, util.ascii_vcode_handler)
    # 初始化远程文件树
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
    return _data.get(_ALIVE)
def set_alive(alive):
    _data[_ALIVE] = alive

# 定义常量
log_file = None
cookie_file = None
cookie_jar = None
client = None
remote_tree = None