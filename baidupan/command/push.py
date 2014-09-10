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

    def execute(self, args):
        if len(args) == 0:
            print 'nothing to push'
        else:
            for local_file in args:
                self.upload_one_file(local_file)

    def upload_one_file(self, fn):
        upload_file = fn if fn.startswith('/') else '%s%s' % (context.get_lwd(), fn)
        if os.path.exists(upload_file) and os.path.isfile(upload_file):
            print 'upload file: %s ...' % upload_file
            result = context.client.upload_curl(context.get_rwd(), upload_file)
            print 'file saved to: %s !' % result.get('path')
        else:
            print 'no such file!'