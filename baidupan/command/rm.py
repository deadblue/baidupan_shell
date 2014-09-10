# -*- coding: utf-8 -*-
'''
Created on 2014/07/16

@author: deadblue
'''

from baidupan.command import Command
from baidupan import context
import json

class RemoveCommand(Command):
    def __init__(self):
        Command.__init__(self, 'rm', True)
    def execute(self, args):
        file_list = []
        for file_id in args:
            # 从缓存中获取文件信息
            file_obj = context.remote_tree.get_file_by_id(file_id)
            if not file_obj: continue
            file_list.append(file_obj['path'])
            # 删除该文件的缓存
            context.remote_tree.remote_file_from_cache(file_id)
        if len(file_list) > 0:
            print 'the following files will be deleted: '
            for file_path in file_list:
                print file_path
        else:
            print 'nothing to delete'
        # 调用API删除文件
        context.client.delete(json.dumps(file_list))

    def get_completer_words(self, prefix):
        file_list = context.remote_tree.list_file(parent_dir=context.get_rwd())
        file_ids = map(lambda x:str(x['fs_id']), file_list)
        return filter(lambda x:len(prefix) == 0 or x.startswith(prefix), file_ids)