# -*- coding: utf-8 -*-
'''
Created on 2014/07/08

@author: deadblue
'''

from baidupan import context, config
from baidupan.command import Command, InvalidArgumentException, \
    CommandExecuteException
import os

class NoSuchRemoteFileException(CommandExecuteException):
    pass

class PullCommand(Command):
    def __init__(self):
        Command.__init__(self, 'pull', True)
    def execute(self, file_ids=None):
        if len(file_ids) == 0: raise InvalidArgumentException()
        if type(file_ids) != list: file_ids = [file_ids]
        for file_id in file_ids:
            file_id = int(file_id)
            # 获取文件信息
            file_obj = context.get_file_from_cache(file_id)
            if file_obj is None:
                print 'No such file: %d' % file_id
                continue
            if file_obj['isdir'] == 0:
                self._download_file(file_obj)
            else:
                self._download_dir(file_obj)
    def _download_file(self, file_obj):
        # 获取保存路径
        save_path = os.path.join(context.get_lwd(), file_obj['server_filename'])
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
    def _download_dir(self, dir_obj):
        raise Exception('暂未实现目录下载！')