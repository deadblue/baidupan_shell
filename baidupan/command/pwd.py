# -*- coding: utf-8 -*-
'''
Created on 2014/07/09

@author: deadblue
'''

from baidupan.command import Command
from baidupan import context

class PrintWorkingDirectoryCommand(Command):
    def __init__(self):
        Command.__init__(self, 'pwd', True)
    def execute(self, arg=None):
        print 'remote: %s' % context.get_rwd()
        print 'local : %s' % context.get_lwd()