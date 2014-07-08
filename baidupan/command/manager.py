# -*- coding: utf-8 -*-
'''
Created on 2014/07/07

@author: deadblue
'''
from baidupan.command.cd_command import ChangeDirectoryCommand
from baidupan.command.lcd_command import LocalChangeDirectoryCommand
from baidupan.command.login_command import LoginCommand
from baidupan.command.ls_command import ListCommand
from baidupan.command.upload_command import UploadCommand

class _Manager():
    def __init__(self):
        self._commands = {}
    def register(self, cmd):
        self._commands[cmd.name] = cmd
    def get_command(self, name):
        return self._commands[name] if self._commands.has_key(name) else None

_instance = _Manager()
_instance.register(LoginCommand())
_instance.register(ListCommand())
_instance.register(ChangeDirectoryCommand())
_instance.register(LocalChangeDirectoryCommand())
_instance.register(UploadCommand())

def get_command(name):
    return _instance.get_command(name)

