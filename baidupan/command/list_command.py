# -*- coding: utf-8 -*-
'''
Created on 2014/07/07

@author: deadblue
'''

from baidupan import api, context
from baidupan.command import Command, manager

class ListCommand(Command):
    def __init__(self):
        Command.__init__(self, 'ls')
    def execute(self, arg=None):
        files = api.client.list(context.get(context.CWD))
        print '%-20s %-16s %s' % ('file_id', 'size', 'name')
        for fl in files['list']:
            print '%-20d %-16d %s' % (fl['fs_id'], fl['size'], fl['server_filename'])

manager.register(ListCommand())