# -*- coding: utf-8 -*-
'''
Created on 2014/07/07

@author: deadblue
'''

from baidupan import context
from baidupan.command import Command
import os

class ChangeDirectoryCommand(Command):
    def __init__(self):
        Command.__init__(self, 'cd')
    def execute(self, arg=None):
        if not arg: arg = '/'
        cwd = context.get(context.CWD)
        if arg.startswith('/'):
            cwd = arg
        else:
            cwd = '%s%s' % (cwd, arg)
            cwd = os.path.abspath(cwd)
            if not cwd.endswith('/'):
                cwd += '/'
        context.put(context.CWD, cwd)
