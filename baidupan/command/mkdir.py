# -*- coding: utf-8 -*-
import logging

from baidupan import context
from baidupan.command import Command

__author__ = 'deadblue'

_logger = logging.getLogger('mkdir')

class CreateDirectoryCommand(Command):
    def __init__(self):
        Command.__init__(self, 'mkdir', True)

    def execute(self, args):
        if len(args) == 0:
            print 'nothing happened...'
        else:
            dir_name = args[0]
            dir_path = dir_name if dir_name.startswith('/') else '%s%s' % (context.get_rwd(), dir_name)
            if context.remote_tree.dir_exists(dir_path):
                print 'dir:%s existed!' % dir_path
            else:
                _logger.debug('create remote dir: %s' % dir_path)
                context.client.create_dir(dir_path)