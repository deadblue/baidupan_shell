# -*- coding: utf-8 -*-
'''
Created on 2014/07/09

@author: deadblue
'''

from baidupan.command import Command
from baidupan import context

class ExitCommand(Command):
    def __init__(self):
        Command.__init__(self, 'exit', False)
    def execute(self, args):
        context.alive = False