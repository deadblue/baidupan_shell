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
    def execute(self, file_ids=None):
        if type(file_ids) != list: file_ids = [file_ids]
        file_list = []
        for file_id in file_ids:
            file_id = int(file_id)
            file_obj = context.get_file_from_cache(file_id)
            if not file_obj: continue
            file_list.append(file_obj['path'])
            context.delete_file_from_cache(file_id)
        if len(file_list) > 0:
            print '以下文件将被删除: '
            for file_path in file_list:
                print file_path
        context.client.delete(json.dumps(file_list))
