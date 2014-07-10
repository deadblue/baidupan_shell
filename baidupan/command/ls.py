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
    def execute(self, arg=None):
        # 按名称降序获取文件列表
        rwd = context.get_rwd()
        result = context.client.list(rwd, order='name', desc=None)
        if result['errno'] == -9: raise NoSuchRemoteDirectory()
        file_list = result['list']
        # 缓存文件列表
        context.cache_file_list(rwd, file_list)
        # 输出文件列表
        self._print_file_list(file_list, arg)
    def _print_file_list(self, files, arg=None):
        print '| %-16s | %-19s | %-10s | %s' % ('file_id', 'modify_time', 'size', 'name')
        print '+%s+%s+%s+%s' % ('-' * 18, '-' * 21, '-' * 12, '-' * 10)
        for fl in files:
            print '| %-16d | %-19s | %10s | %s' % (fl['fs_id'],
                                      util.format_time(fl['server_mtime']),
                                      util.format_size(fl['size']), 
                                      fl['server_filename'])
