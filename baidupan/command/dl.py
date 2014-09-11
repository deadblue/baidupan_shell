# -*- coding: utf-8 -*-
'''
Created on 2014/08/19

@author: deadblue
'''

from baidupan import context
from baidupan.command import Command
import os

class CloudDownloadCommand(Command):
    def __init__(self):
        Command.__init__(self, 'dl', True)

    def execute(self, args):
        if len(args) == 0:
            print 'nothing to download'
        else:
            self._download(args[0])
    def _download(self, source):
        task_id = None
        if source.startswith('http:') or source.startswith('https:'):
            task_id = self._download_http(source)
        # elif source.startswith('ftp:'):
        #     task_id = self._download_ftp(source)
        elif source.startswith('ed2k:'):
            task_id = self._download_ed2k(source)
        # elif source.startswith('magnet:'):
        #     task_id = self._download_magnet(source)
        elif source.endswith('.torrent'):
            task_id = self._download_torrent(source)
        else:
            print 'unsupported source!'
        if task_id:
            task_id = str(task_id)
            result = context.client.cloud_dl_query_task(task_id)
            task_info = result['task_info'][task_id]
            if task_info.has_key('task_name') and task_info.has_key('finished_size') and task_info.has_key('file_size'):
                finished_present = 100.0 * int(task_info['finished_size']) / int(task_info['file_size'])
                print 'task: %s / progress: %.2f%%' % (task_info['task_name'], finished_present)
        else:
            print 'can not create download task!'
    def _download_http(self, link):
        print 'create download for http ...'
        result = context.client.cloud_dl_add_http_task(link, context.get_rwd())
        task_id = result['task_id'] if result.has_key('task_id') else None
        return task_id
    def _download_ed2k(self, link):
        print 'create download for ed2k ...'
        result = context.client.cloud_dl_add_ed2k_task(link, context.get_rwd())
        task_id = result['task_id'] if result.has_key('task_id') else None
        return task_id
    def _download_torrent(self, torrent_file):
        source_path = None
        # 从网盘上查找种子文件
        result = context.client.list(context.get_rwd())
        file_objs = result['list']
        for file_obj in file_objs:
            if file_obj['server_filename'] == torrent_file.decode('utf-8'):
                source_path = file_obj['path']
                break
        # 若网盘上不存在则从本地查找
        if source_path is None:
            torrent_file = os.path.join(context.get_lwd(), torrent_file)
            if os.path.exists(torrent_file):
                # 若本地存在，则上传到网盘
                print 'upload torrent file: %s ...' % torrent_file
                result = context.client.upload(context.get_rwd(), torrent_file)
                source_path = result['path']
            else:
                # do nothing?
                pass
        if source_path is None:
            print 'no such torrent file!'
            return None
        else:
            # 创建bt任务
            print 'query torrent info ...'
            result = context.client.cloud_dl_query_bt_info(source_path)
            bt_info = result['torrent_info']
            print 'create download for bt ...'
            # 选择种子中的全部文件
            selected_idx = map(lambda x:str(x+1), xrange(0, bt_info['file_count']))
            selected_idx = ','.join(selected_idx)
            # 创建离线下载任务
            result = context.client.cloud_dl_add_bt_task(source_path, selected_idx, bt_info['sha1'], context.get_rwd())
            task_id = result['task_id'] if result.has_key('task_id') else None
            return task_id