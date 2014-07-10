# -*- coding: utf-8 -*-
'''
Created on 2014/07/08

@author: deadblue
'''

from baidupan import context
from baidupan.command import Command, InvalidArgumentException, \
    CommandExecuteException
import os

class NoSuchRemoteFileException(CommandExecuteException):
    pass

class DownloadCommand(Command):
    def __init__(self):
        Command.__init__(self, 'download', True)
    def execute(self, file_id=None):
        if file_id is None:
            raise InvalidArgumentException()
        file_id = int(file_id)
        # 获取文件信息
        file_obj = context.get_file_from_cache(file_id)
        if file_obj is None:
            raise NoSuchRemoteFileException()
        # 获取保存路径
        save_path = os.path.join(context.get_lwd(), file_obj['server_filename'])
        context.client.download(file_id, save_path)