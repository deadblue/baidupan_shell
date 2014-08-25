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
    def _print_file_list(self, files, ext=None):
        print '| %-16s | %-19s | %-10s | %s' % ('file_id', 'modify_time', 'size', 'name')
        print '+%s+%s+%s+%s' % ('-' * 18, '-' * 21, '-' * 12, '-' * 10)
        for fl in files:
            if not self._filter_file(fl, ext): continue
            file_size = '<DIR>' if fl['isdir'] == 1 else util.format_size(fl['size'])
            print '| %-16d | %-19s | %10s | %s' % (fl['fs_id'],
                                      util.format_time(fl['server_mtime']),
                                      file_size, fl['server_filename'])
    def _filter_file(self, file_obj, ext=None):
        if ext is None or len(ext) == 0:
            return True
        if type(ext) is str: ext = [ext]
        if file_obj['isdir'] == 1:
            return 'dir' in ext
        else:
            file_name = file_obj['server_filename']
            dot = file_name.rfind('.')
            if dot >= 0:
                file_ext = file_name[(dot+1):]
                return file_ext in ext
            else:
                return False