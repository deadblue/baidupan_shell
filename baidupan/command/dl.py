# -*- coding: utf-8 -*-
'''
Created on 2014/08/19

@author: deadblue
'''

import json
import os
import logging

from baidupan import context, bt
from baidupan.command import Command

_logger = logging.getLogger('dl')

class CloudDownloadCommand(Command):
    def __init__(self):
        Command.__init__(self, 'dl', True)

    def execute(self, args):
        if len(args) == 0:
            print 'nothing to download'
        else:
            # 判断是否需要混淆名称
            mask = '--mask' in args
            self._download(args[-1], mask)

    def _download(self, source, mask=False):
        task_id = None
        if source.startswith('http:') or source.startswith('https:'):
            task_id = self._download_http(source)
        elif source.startswith('ed2k:'):
            task_id = self._download_ed2k(source)
        elif source.endswith('.torrent'):
            task_id = self._download_torrent(source, mask)
        # elif source.startswith('ftp:'):
        #     task_id = self._download_ftp(source)
        # elif source.startswith('magnet:'):
        #     task_id = self._download_magnet(source)
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
    def _download_torrent(self, torrent_file, mask=False):
        save_path = context.get_rwd()
        source_path = None
        # 查找种子文件
        torrent_file = os.path.join(context.get_lwd(), torrent_file)
        if os.path.exists(torrent_file):
            if not mask:
                # 上传种子文件
                print 'upload torrent file: %s ...' % torrent_file
                result = context.client.upload(context.get_rwd(), torrent_file)
                source_path = result['path']
            else:
                print 'mask torrent file ...'
                # 混淆bt文件
                torrent_data, name_dict = bt.mask_file(torrent_file)
                # 创建一层目录，作为下载存储目录
                save_path = '%s%s/' % (save_path, name_dict['prefix'])
                _logger.debug('save path: %s' % save_path)
                context.client.create_dir(save_path)
                # 上传混淆后的种子文件
                print 'upload masked torrent ...'
                result = context.client.upload_data(save_path, 'tmp.torrent', torrent_data)
                source_path = result['path']
                # 上传文件名字典
                print 'upload name dictionary ...'
                dict_data = json.dumps(name_dict)
                context.client.upload_data(save_path, 'dictionary.txt', dict_data)
        else:
            print 'no such torrent file!'
            return None
        # 获取种子文件信息
        print 'query torrent info ...'
        result = context.client.cloud_dl_query_bt_info(source_path)
        bt_info = result.get('torrent_info')
        # 创建bt任务
        task_id = None
        if bt_info is None:
            print 'can\'t get torrent info!'
        else:
            print 'create download for bt ...'
            # 选择种子中的全部文件
            selected_idx = map(lambda x:str(x+1), xrange(0, bt_info['file_count']))
            selected_idx = ','.join(selected_idx)
            # 创建离线下载任务
            result = context.client.cloud_dl_add_bt_task(source_path, selected_idx, bt_info['sha1'], save_path)
            task_id = result['task_id'] if result.has_key('task_id') else None
        # 删除种子文件
        print 'delete torrent file ...'
        context.client.delete(json.dumps([source_path]))
        return task_id