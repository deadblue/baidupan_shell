# -*- coding: utf-8 -*-
'''
Created on 2014/07/07

@author: deadblue
'''

from baidupan import context, path
from baidupan.command import Command
import os

class ChangeDirectoryCommand(Command):
    def __init__(self):
        Command.__init__(self, 'cd', True)

    def execute(self, args):
        target_dir = args[0] if len(args) > 0 else '/'
        rwd = context.get_rwd()
        if target_dir.startswith('/'):
            rwd = target_dir
        else:
            rwd = '%s%s' % (rwd, target_dir)
            rwd = path.remote_abspath(rwd)
        if not rwd.endswith('/'): rwd += '/'
        context.set_rwd(rwd)

    def get_completer_words(self, prefix):
        '''
        TODO 自动完成存在问题，推测与unicode有关
        '''
        # 获取要寻址的路径
        if prefix.startswith('/'):
            rwd = prefix
        else:
            if prefix is None: prefix = ''
            rwd = '%s%s' % (context.get_rwd(), prefix)
        # 处理路径中的相对路径
        if rwd.endswith('/'):
            lwd = os.path.abspath(rwd) + '/'
        else:
            lwd = os.path.abspath(rwd)
        # 拆分出父目录和子目录前缀
        parent_dir, sub_prefix = os.path.split(lwd)
        # 从缓存中获取父目录下的所有子目录
        if not context.has_dir_cache(parent_dir):
            result = context.client.list(parent_dir)
            context.cache_file_list(parent_dir, result['list'])
        sub_dirs = context.get_dir_from_cache(parent_dir)
        # 只保留名称
        sub_dirs = map(lambda x:x['server_filename'], sub_dirs)
        # 列出所有符合前缀的子目录
        return filter(lambda x:unicode(x).startswith(unicode(sub_prefix)), sub_dirs)