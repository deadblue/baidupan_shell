# -*- coding: utf-8 -*-
'''
Created on 2014/07/06

@author: deadblue
'''

import os
import pickle

__all__ = ['put', 'get', 'save']

class _Config():
    '''
    需要持久化存储的内容
    '''
    def __init__(self):
        self._data = {}
        self._config_file = os.path.join(os.getenv('HOME'), '.baidu_lixian.config')
        if os.path.exists(self._config_file):
            self._data = pickle.load(open(self._config_file, 'r'))
    def put(self, name, value):
        self._data[name] = value
    def get(self, name):
        return self._data.get(name)
    def save(self):
        pickle.dump(self._data, open(self._config_file, 'w'))

_instance = _Config()

def put(name, value):
    _instance.put(name, value)

def get(name):
    return _instance.get(name)

def save():
    _instance.save()