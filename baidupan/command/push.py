# -*- coding: utf-8 -*-
'''
Created on 2014/07/07

@author: deadblue
'''

from baidupan import context
from baidupan.command import Command, InvalidArgumentException
import os

class PushCommand(Command):

    def __init__(self):
        Command.__init__(self, 'push', True)

    def execute(self, args=None):
        if args is None:
            print 'nothing to push'
            return
        if type(args) is str:
            self.upload_one_file(args)
        else:
            for arg in args:
                self.upload_one_file(arg)

    def upload_one_file(self, fn):
        upload_file = fn if fn.startswith('/') else '%s%s' % (context.get_lwd(), fn)
        if os.path.exists(upload_file) and os.path.isfile(upload_file):
            print 'upload file: %s ...' % upload_file
            result = context.client.upload_curl(context.get_rwd(), upload_file)
            print 'file saved to: %s !' % result.get('path')
        else:
            print 'no such file!'