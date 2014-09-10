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
        # 按名称降序获取文件列表
        rwd = context.get_rwd()
        show_dir = len(args) == 0 or 'dir' in args
        file_list = context.remote_tree.list(rwd, show_dir=show_dir, show_file=True,
                                             show_exts=args, force_fetch=True)
        self._print_file_list(file_list)
    def _print_file_list(self, files):
        print '| %-16s | %-19s | %-10s | %s' % ('file_id', 'modify_time', 'size', 'name')
        print '+%s+%s+%s+%s' % ('-' * 18, '-' * 21, '-' * 12, '-' * 10)
        for fl in files:
            file_size = '<DIR>' if fl['isdir'] == 1 else util.format_size(fl['size'])
            print '| %-16d | %-19s | %10s | %s' % (fl['fs_id'],
                                      util.format_time(fl['server_mtime']),
                                      file_size, fl['server_filename'])