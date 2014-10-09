# -*- coding: utf-8 -*-
'''
Created on 2014/07/07

@author: deadblue
'''

from baidupan import context, util
from baidupan.command import Command, CommandExecuteException

class NoSuchRemoteDirectory(CommandExecuteException):
    pass

class ListCommand(Command):
    def __init__(self):
        Command.__init__(self, 'ls', True)
    def execute(self, args):
        # 处理过滤条件
        show_dir = len(args) == 0 or 'dir' in args
        show_file = not ('dir' in args and len(args) == 1)
        exts = filter(lambda x:x!='dir', args)
        file_list = context.remote_tree.list(context.get_rwd(),
                                             show_dir=show_dir, show_file=show_file,
                                             show_exts=exts, force_fetch=True)
        self._print_file_list(file_list)
    def _print_file_list(self, files):
        print '| %-16s | %-10s | %s' % ('file_id', 'size', 'name')
        print '+%s+%s+%s' % ('-' * 18, '-' * 12, '-' * 10)
        for fl in files:
            file_size = '<DIR>' if fl['isdir'] == 1 else util.format_size(fl['size'])
            print '| %-16d | %10s | %s' % (fl['fs_id'], file_size, fl['server_filename'])