# -*- coding: utf-8 -*-
'''
Created on 2014/07/07

@author: deadblue
'''

class InvalidArgumentException(Exception):
    pass

class CommandExecuteException(Exception):
    pass

class Command():
    def __init__(self, name, need_login):
        self.name = name
        self.need_login = need_login
    def execute(self, arg=None):
        pass
    def get_completer_words(self, prefix):
        return []