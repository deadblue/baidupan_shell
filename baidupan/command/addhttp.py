# -*- coding: utf-8 -*-
'''
Created on 2014/08/16

@author: deadblue
'''
from baidupan.command import Command


class AddHTTPCommand(Command):
    def __init__(self):
        Command.__init__(self, 'addhttp', True)
    def execute(self, arg=None):
        pass