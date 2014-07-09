# -*- coding: utf-8 -*-
'''
Created on 2014/07/07

@author: deadblue
'''

from baidupan.command.cd_command import ChangeDirectoryCommand
from baidupan.command.debug_command import DebugCommand
from baidupan.command.download_command import DownloadCommand
from baidupan.command.exit_command import ExitCommand
from baidupan.command.lcd_command import LocalChangeDirectoryCommand
from baidupan.command.login_command import LoginCommand
from baidupan.command.ls_command import ListCommand
from baidupan.command.upload_command import UploadCommand

class _Manager():
    def __init__(self):
        self._commands = {}
    def register(self, cmd):
        self._commands[cmd.name] = cmd
    def get_command_names(self):
        return self._commands.keys()
    def get_command(self, name):
        return self._commands[name] if self._commands.has_key(name) else None

_instance = _Manager()
_instance.register(LoginCommand())
_instance.register(ListCommand())
_instance.register(ChangeDirectoryCommand())
_instance.register(LocalChangeDirectoryCommand())
_instance.register(UploadCommand())
_instance.register(DownloadCommand())
_instance.register(ExitCommand())
_instance.register(DebugCommand())

def get_command_names():
    return _instance.get_command_names()

def parse_input(line):
    pos = line.find(' ')
    cmd_name = line if pos < 0 else line[0:pos]
    args = None if pos < 0 else line[pos+1:]
    cmd = _instance.get_command(cmd_name)
    return cmd, args
