# -*- coding: utf-8 -*-
'''
Created on 2014/07/05

@author: deadblue
'''

from baidupan import api

class Context():
    '''
    运行时内容，不需要持久化
    '''
    def __init__(self):
        self._cache = {
                       'work_dir' : '/'
                       }
    def put(self, name, value):
        self._cache[name] = value
    def get(self, name):
        return self._cache.get(name)

client = api.BaiduPanClient()
context = Context()