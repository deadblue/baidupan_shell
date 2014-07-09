# -*- coding: utf-8 -*-
'''
Created on 2014/07/06

@author: deadblue
'''

import os

# 远端当前路径
_RWD = 'rwd'
# 本地当前路径
_LWD = 'lwd'

# 上下文数据
_data = {
         _RWD : '/',
         _LWD : os.getcwd()
         }
# 目录缓存
_dir_cache = {}
# 文件缓存
_file_cache = {}

alive = True

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

def get_dir_from_cache(parent_dir):
    return _dir_cache.get(parent_dir)
def add_dir_to_cache(parent_dir, dir_obj):
    sub_dirs = _dir_cache.get(parent_dir)
    if not sub_dirs:
        sub_dirs = []
        _dir_cache[parent_dir] = sub_dirs
    sub_dirs.append(dir_obj)

def get_file_from_cache(file_id):
    return _file_cache.get(file_id)
def add_file_to_cache(file_obj):
    _file_cache[file_obj['fs_id']] = file_obj
