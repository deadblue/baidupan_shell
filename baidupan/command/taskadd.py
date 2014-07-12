# -*- coding: utf-8 -*-
'''
Created on 2014/07/13

@author: deadblue
'''

from baidupan.command import Command
from baidupan import context
import os

class CloudTaskAddCommand(Command):
    def __init__(self):
        Command.__init__(self, 'taskadd', True)
    def execute(self, torrent_file):
        # 上传种子文件，获取上传后的保存路径
        print '上传种子文件 %s ...' % torrent_file
        torrent_file = os.path.join(context.get_lwd(), torrent_file)
        result = context.client.upload(context.get_rwd(), torrent_file)
        source_path = result['path']
        # 查询种子文件信息
        print '获取种子文件信息...'
        result = context.client.cloud_dl_query_bt_info(source_path)
        bt_info = result['torrent_info']
        print '创建离线下载任务...'
        # 下载种子中的全部文件
        selected_idx = map(lambda x:str(x+1), xrange(0, bt_info['file_count']))
        selected_idx = ','.join(selected_idx)
        # 创建离线下载任务
        result = context.client.cloud_dl_add_bt_task(source_path, selected_idx, bt_info['sha1'], context.get_rwd())
        task_id = result['task_id']
        # 查询任务信息
        result = context.client.cloud_dl_query_task(task_id)
        task_info = result['task_info'][str(task_id)]
        finished_present = 100.0 * int(task_info['finished_size']) / int(task_info['file_size'])
        print '任务名称: %s / 进度：%.2f%%' % (task_info['task_name'], finished_present)