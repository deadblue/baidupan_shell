# -*- coding: utf-8 -*-
'''
Created on 2014/07/07

@author: deadblue
'''
from baidupan import context
from baidupan.command import Command
import os

class LocalChangeDirectoryCommand(Command):
    def __init__(self):
        Command.__init__(self, 'lcd', False)
    def execute(self, arg=None):
        if not arg: arg = '/'
        lwd = context.get_lwd()
        if arg.startswith('/'):
            lwd = arg
        else:
            lwd = '%s%s' % (lwd, arg)
            lwd = os.path.abspath(lwd)
            if not lwd.endswith('/'):
                lwd += '/'
        context.set_lwd(lwd)
