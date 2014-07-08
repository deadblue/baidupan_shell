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
        Command.__init__(self, 'cd', True)
    def execute(self, arg=None):
        if not arg: arg = '/'
        rwd = context.get_rwd()
        if arg.startswith('/'):
            rwd = arg
        else:
            rwd = '%s%s' % (rwd, arg)
            rwd = os.path.abspath(rwd)
            if not rwd.endswith('/'):
                rwd += '/'
        context.set_rwd(rwd)
