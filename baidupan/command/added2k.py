# -*- coding: utf-8 -*-
'''
Created on 2014/08/16

@author: deadblue
'''

from baidupan.command import Command

class AddED2KCommand(Command):
    def __init__(self):
        Command.__init__(self, 'added2k', True)
    def execute(self, arg=None):
        pass