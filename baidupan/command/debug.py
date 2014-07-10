# -*- coding: utf-8 -*-
'''
Created on 2014/07/09

@author: deadblue
'''

from baidupan.command import Command
from baidupan import context

class DebugCommand(Command):
    def __init__(self):
        Command.__init__(self, 'debug', False)
    def execute(self, arg=None):
        print 'login: %r' % context.client.is_login
        if context.client.is_login:
            print 'user name: %s' % context.client.user_name
        # TODO：输出缓存信息
