# -*- coding: utf-8 -*-
'''
Created on 2014/07/08

@author: deadblue
'''

import os

from baidupan import context, config
from baidupan.command import Command

class PullCommand(Command):
    def __init__(self):
        Command.__init__(self, 'pull', True)

    def execute(self, args):
        save_path = context.get_lwd()
        for file_id in args:
            # 获取文件信息
            file_obj = context.remote_tree.get_file_by_id(file_id)
            if file_obj is None:
                print 'no such file: %s' % file_id
                continue
            if file_obj['isdir'] == 0:
                print 'pull file: %s ...' % file_obj['server_filename']
                self._download_file(file_obj, save_path)
            else:
                print 'pull dir: %s ...' % file_obj['server_filename']
                self._download_dir(file_obj, save_path)
    def _download_file(self, file_obj, save_path):
        # 获取保存路径
        save_path = os.path.join(save_path, file_obj['server_filename'])
        # 下载请求
        download_req = context.client.get_download_request(file_obj['fs_id'])
        # 调用用户配置的下载器进行下载
        dler = config.get_downloader()
        if dler in ['aria', 'aria2c']:
            from baidupan.downloader import aria2c
            aria2c.download(download_req, save_path)
        elif dler == 'wget':
            from baidupan.downloader import wget
            wget.download(download_req, save_path)
        else:
            # 默认情况下使用curl
            from baidupan.downloader import curl
            curl.download(download_req, save_path)
    def _download_dir(self, dir_obj, save_path):
        # 在本地创建目录
        save_path = os.path.join(save_path, dir_obj['server_filename'])
        os.makedirs(save_path)
        # 遍历子文件，开始下载
        sub_objs = context.remote_tree.list(parent_dir=dir_obj['path'], force_fetch=True)
        for sub_obj in sub_objs:
            if sub_obj['isdir'] != 0:
                self._download_dir(sub_obj, save_path)
            else:
                self._download_file(sub_obj, save_path)

    def get_completer_words(self, prefix):
        file_list = context.remote_tree.list(parent_dir=context.get_rwd(), force_fetch=False)
        file_ids = map(lambda x:'%d ' % x['fs_id'], file_list)
        return filter(lambda x:len(prefix) == 0 or x.startswith(prefix), file_ids)