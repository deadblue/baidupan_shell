# -*- coding: utf-8 -*-
import logging

__author__ = 'deadblue'

import json

from baidupan import context
from baidupan.command import Command

_logger = logging.getLogger('unmask')

class UnmaskCommand(Command):
    def __init__(self):
        Command.__init__(self, 'unmask', True)
    def execute(self, args):
        if args is None or len(args) == 0:
            print 'nothing to unmask'
            return
        target_dir = args[0]
        dir_objs = context.remote_tree.list_dir(context.get_rwd())
        for dir_obj in dir_objs:
            if dir_obj['server_filename'].encode('utf-8') == target_dir:
                self._unmask_start(dir_obj)
                break
    def _unmask_start(self, dir_obj):
        if dir_obj['isdir'] == 0:
            print 'target is not a directory!'
            return
        # 查找字典文件
        print 'load dictionary ...'
        dic_file_id = False
        sub_objs = context.remote_tree.list(dir_obj['path'], show_dir=True, show_file=True, force_fetch=True)
        for sub_obj in sub_objs:
            file_name = sub_obj['server_filename'].encode('utf-8')
            if file_name == 'dictionary.txt':
                dic_file_id = sub_obj['fs_id']
                break
        if not dic_file_id:
            print 'can not find dictionary.txt'
            return
        # 读取字典数据
        dic_data = context.client.download_data(dic_file_id)
        dic_data = json.loads(dic_data)
        prefix, names = dic_data['prefix'], dic_data['names']
        name_dic = {}
        for i in xrange(len(names)):
            key = '%s_%d' % (prefix, i + 1)
            name_dic[key] = names[i]
        # 重新遍历文件，处理重命名
        print 'start unmask ...'
        for sub_obj in sub_objs:
            file_name = sub_obj['server_filename'].encode('utf-8')
            if not name_dic.has_key(file_name): continue
            if sub_obj['isdir'] == 0:
                self._unmask_file(sub_obj, name_dic)
            else:
                self._unmask_dir(sub_obj, name_dic)
        print 'unmask complete!'
    def _unmask_dir(self, dir_obj, name_dic):
        # 查询下级文件列表
        sub_objs = context.remote_tree.list(dir_obj['path'], show_dir=True, show_file=True, force_fetch=True)
        # 先重命名下级文件
        for sub_obj in sub_objs:
            file_name = sub_obj['server_filename'].encode('utf-8')
            if not name_dic.has_key(file_name): continue
            if sub_obj['isdir'] == 0:
                self._unmask_file(sub_obj, name_dic)
            else:
                self._unmask_dir(sub_obj, name_dic)
        # 重命名目录
        file_name = dir_obj['server_filename'].encode('utf-8')
        print 'rename: %s => %s' % (file_name, name_dic[file_name])
        context.remote_tree.rename(dir_obj['path'], name_dic[file_name])
    def _unmask_file(self, file_obj, name_dic):
        file_name = file_obj['server_filename'].encode('utf-8')
        print 'rename: %s => %s' % (file_name, name_dic[file_name])
        context.remote_tree.rename(file_obj['path'], name_dic[file_name])
