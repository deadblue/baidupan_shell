# -*- coding: utf-8 -*-
'''
Created on 2014/07/06

@author: deadblue
'''

PWD = 'pwd'
LWD = 'lwd'

class _Context():
    '''
    运行时内容，不需要持久化
    '''
    def __init__(self):
        self._cache = {
                       PWD : '/',
                       LWD : '/'
                       }
    def put(self, name, value):
        self._cache[name] = value
    def get(self, name):
        return self._cache.get(name)

_instance = _Context()

def put(name, value):
    _instance.put(name, value)

def get(name):
    return _instance.get(name)