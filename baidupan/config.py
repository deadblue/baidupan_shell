# -*- coding: utf-8 -*-
'''
Created on 2014/07/13

@author: deadblue
'''

import os
from baidupan import util
import pickle

_DOWNLOADER = 'downloader'
_DOWNLOADER_DEFAULT = 'curl'
_LOCALHOME = 'localhome'
_LOCALHOME_DEFAULT = '%s%s' % (os.getcwd(), os.sep)

_config_file = util.get_data_file('.baidupan.config')

class _Config():
    def __init__(self):
        self._data = {}
    def load(self):
        if os.path.exists(_config_file):
            fp = open(_config_file, 'r')
            self._data = pickle.load(fp)
            fp.close()
    def save(self):
        fp = open(_config_file, 'w')
        pickle.dump(self._data, fp)
        fp.close()
    def get(self, name, def_value=None):
        return self._data.get(name, def_value)
    def put(self, name, value):
        self._data[name] = value

_instance = _Config()

def load():
    _instance.load()
def save():
    _instance.save()
def get_all():
    return _instance._data
def get(name):
    return _instance.get(name, None)
def put(name, value):
    _instance.put(name, value)

def get_downloader():
    return _instance.get(_DOWNLOADER, _DOWNLOADER_DEFAULT)
def get_localhome():
    return _instance.get(_LOCALHOME, _LOCALHOME_DEFAULT)
