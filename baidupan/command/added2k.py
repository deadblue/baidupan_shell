# -*- coding: utf-8 -*-
'''
Created on 2014/08/16

@author: deadblue
'''

from baidupan import context
from baidupan.command import Command

class AddED2KCommand(Command):
    def __init__(self):
        Command.__init__(self, 'added2k', True)
    def execute(self, link=None):
        if link is None: return
        # 创建离线任务
        print 'Create cloud download task ...'
        result = context.client.cloud_dl_add_ed2k_task(link, context.get_rwd())
        task_id = result['task_id']
        # 查询任务信息
        result = context.client.cloud_dl_query_task(task_id)
        task_info = result['task_info'][str(task_id)]
        finished_present = 100.0 * int(task_info['finished_size']) / int(task_info['file_size'])
        print 'Task: %s / Progress: %.2f%%' % (task_info['task_name'], finished_present)