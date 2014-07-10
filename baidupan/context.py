# -*- coding: utf-8 -*-
'''
Created on 2014/07/06

@author: deadblue
'''

import os
from baidupan import api

# 远端当前路径
_RWD = 'rwd'
# 本地当前路径
_LWD = 'lwd'

# 上下文数据
_data = {
         _RWD : '/',
         _LWD : '%s%s' % (os.getcwd(), os.sep)
         }
# 目录缓存
_dir_cache = {}
# 文件缓存
_file_cache = {}

# 终端活动标记
alive = True
# 百度盘客户端实例
client = api.BaiduPanClient()

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
