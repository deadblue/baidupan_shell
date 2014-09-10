# -*- coding: utf-8 -*-
'''
Created on 2014/07/17

@author: deadblue
'''

from baidupan.command import Command
from baidupan import context, util

class TaskListCommand(Command):
    def __init__(self):
        Command.__init__(self, 'tasks', True)
    def execute(self, args):
        # 获取离线任务列表
        result = context.client.cloud_dl_list_task()
        task_ids = map(lambda x:x['task_id'], result['task_info'])
        task_ids = ','.join(task_ids)
        # 查询离线任务详细信息
        result = context.client.cloud_dl_query_task(task_ids)
        self._print_tasks(result['task_info'])
    def _print_tasks(self, tasks):
        print '| %-16s | %-19s | %-7s | %s ' % ('task_id', 'create_time', 'precent', 'name')
        print '+%s+%s+%s+%s' % ('-' * 18, '-' * 21, '-' * 9, '-' * 10)
        for task_id, task_info in tasks.items():
            create_time = int(task_info['create_time'])
            dl_per = 100.0 * int(task_info['finished_size']) / int(task_info['file_size'])
            print '| %-16s | %-19s | %6.2f%% | %s' % (task_id,
                                                      util.format_time(create_time),
                                                      dl_per, 
                                                      task_info['task_name']
                                                      )