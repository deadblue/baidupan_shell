# -*- coding: utf-8 -*-
'''
Created on 2014/07/07

@author: deadblue
'''

class InvalidArgumentException(Exception):
    pass

class Command():
    def __init__(self, name):
        self.name = name
    def execute(self, arg=None):
        pass