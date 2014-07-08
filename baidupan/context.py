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

class _Context():
    '''
    运行时内容，不需要持久化
    '''
    def __init__(self):
        self._data = {
                       _RWD : '/',
                       _LWD : os.getcwd()
                       }
    def put(self, name, value):
        self._data[name] = value
    def get(self, name):
        return self._data.get(name)

_instance = _Context()

def get(name):
    return _instance.get(name)
def put(name, value):
    _instance.put(name, value)

def get_rwd():
    return _instance.get(_RWD)
def set_rwd(value):
    _instance.put(_RWD, value)

def get_lwd():
    return _instance.get(_LWD)
def set_lwd(value):
    _instance.put(_LWD, value)

is_login = False