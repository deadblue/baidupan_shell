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

    def execute(self, args):
        for file_id in args:
            # 获取文件信息
            file_obj = context.remote_tree.get_file_by_id(file_id)
            if file_obj is None:
                print 'no such file: %s' % file_id
                continue
            if file_obj['isdir'] == 0:
                self._download_file(file_obj)
            else:
                self._download_dir(file_obj)
    def _download_file(self, file_obj):
        file_name = file_obj['server_filename'].encode('utf-8')
        print 'pull file: %s ...' % file_name
        # 获取保存路径
        save_path = os.path.join(context.get_lwd(), file_name)
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
        raise Exception('unimplement!')

    def get_completer_words(self, prefix):
        file_list = context.remote_tree.list_file(parent_dir=context.get_rwd())
        file_ids = map(lambda x:'%d ' % x['fs_id'], file_list)
        return filter(lambda x:len(prefix) == 0 or x.startswith(prefix), file_ids)