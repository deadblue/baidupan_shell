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
            cache_dirs = context.get_dir_from_cache(context.get_rwd())
            # 判断目录是否已存在
            if dir_name in map(lambda x:x['server_filename'], cache_dirs):
                _logger.error('target dir existed!')
            else:
                dir_path = '%s%s' % (context.get_rwd(), dir_name)
                _logger.debug('create remote dir: %s' % dir_path)
                context.client.create_dir(dir_path)