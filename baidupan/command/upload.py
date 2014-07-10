# -*- coding: utf-8 -*-
'''
Created on 2014/07/07

@author: deadblue
'''

from baidupan import context
from baidupan.command import Command, InvalidArgumentException
import os

class UploadCommand(Command):
    def __init__(self):
        Command.__init__(self, 'upload', True)
    def execute(self, arg=None):
        if arg is None: raise InvalidArgumentException()
        upload_file = arg if arg.startswith('/') else '%s%s' % (context.get_lwd(), arg)
        if os.path.exists(upload_file) and os.path.isfile(upload_file):
            context.client.upload_curl(context.get_rwd(), upload_file)
        else:
            raise InvalidArgumentException()
