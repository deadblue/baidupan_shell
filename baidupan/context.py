# -*- coding: utf-8 -*-
'''
Created on 2014/07/06

@author: deadblue
'''

import logging
import os
import sys
from baidupan import util, config

# 远端当前路径
_RWD = 'rwd'
# 本地当前路径
_LWD = 'lwd'
# 上下文数据
_data = {}

def init():
    # 解析运行参数
    args = util.parser_arguments(sys.argv[1:])
    log_level = logging.DEBUG if args.get('debug') else logging.ERROR
    # 设置日志级别
    logging.basicConfig(level=log_level, stream=sys.stdout,
                        format='%(levelname)s %(name)s - %(message)s')
    _data[_RWD] = '/'
    _data[_LWD] = config.get_localhome()
    # 标记为活动
    global alive
    alive = True
    # 初始化client
    import cookielib
    from baidupan import api, tree
    global cookie_file, cookie_jar, client, remote_tree
    cookie_file = util.get_data_file('.baidupan.cookie')
    cookie_jar = cookielib.MozillaCookieJar(cookie_file)
    if os.path.exists(cookie_file): cookie_jar.load()
    client = api.BaiduPanClient(cookie_jar, util.vcode_handler)
    remote_tree = tree.RemoteTree(client)

def put(name, value):
    _data[name] = value
def get(name):
    return _data.get(name)
def get_rwd():
    return get(_RWD)
def set_rwd(value):
    put(_RWD, value)
def get_lwd():
    return get(_LWD)
def set_lwd(value):
    put(_LWD, value)

# 目录缓存
_dir_cache = {}
# 文件缓存
_file_cache = {}

def has_dir_cache(parent_dir):
    return _dir_cache.has_key(parent_dir)
def cache_file_list(parent_dir, files):
    sub_dirs = []
    for fl_obj in files:
        _file_cache[ fl_obj['fs_id'] ] = fl_obj
        if fl_obj['isdir'] == 1:
            sub_dirs.append(fl_obj)
    _dir_cache[parent_dir] = sub_dirs
def get_dir_from_cache(parent_dir):
    return _dir_cache.get(parent_dir)
def get_file_from_cache(file_id):
    return _file_cache.get(file_id)
def delete_file_from_cache(file_id):
    if _file_cache.has_key(file_id):
        del _file_cache[file_id]

# 定义常量
alive = None
cookie_file = None
cookie_jar = None
client = None
remote_tree = None