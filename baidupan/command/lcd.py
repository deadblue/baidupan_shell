# -*- coding: utf-8 -*-
'''
Created on 2014/07/07

@author: deadblue
'''

from baidupan import context
from baidupan.command import Command
import os

class LocalChangeDirectoryCommand(Command):
    def __init__(self):
        Command.__init__(self, 'lcd', False)
    def execute(self, arg=None):
        if not arg: arg = '/'
        lwd = context.get_lwd()
        if arg.startswith('/'):
            lwd = arg
        else:
            lwd = '%s%s' % (lwd, arg)
            lwd = os.path.abspath(lwd)
        if not lwd.endswith('/'):
            lwd += '/'
        # 设置本地工作目录
        if os.path.exists(lwd):
            context.set_lwd(lwd)
        else:
            print 'No such path!'
    def get_completer_words(self, prefix):
        # 获取要寻址的路径
        if prefix.startswith('/'):
            lwd = prefix
        else:
            if prefix is None: prefix = ''
            lwd = '%s%s' % (context.get_lwd(), prefix)
        # 处理路径中的相对路径
        if lwd.endswith('/'):
            lwd = os.path.abspath(lwd) + '/'
        else:
            lwd = os.path.abspath(lwd)
        # 拆分出父目录和子目录前缀
        parent_dir, sub_prefix = os.path.split(lwd)
        # 列出父目录下所有目录
        sub_dirs = os.listdir(parent_dir)
        # 列出所有符合前缀的子目录
        sub_dirs = filter(lambda x:x.startswith(sub_prefix), sub_dirs)
        return map(lambda x:'%s/' % x, sub_dirs)
