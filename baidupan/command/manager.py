# -*- coding: utf-8 -*-
'''
Created on 2014/07/07

@author: deadblue
'''

from baidupan.command.cd import ChangeDirectoryCommand
from baidupan.command.conf import ConfigCommand
from baidupan.command.debug import DebugCommand
from baidupan.command.download import DownloadCommand
from baidupan.command.exit import ExitCommand
from baidupan.command.lcd import LocalChangeDirectoryCommand
from baidupan.command.login import LoginCommand
from baidupan.command.ls import ListCommand
from baidupan.command.play import PlayCommand
from baidupan.command.pwd import PrintWorkingDirectoryCommand
from baidupan.command.taskadd import CloudTaskAddCommand
from baidupan.command.upload import UploadCommand
from baidupan import util

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
_instance.register(ConfigCommand())
_instance.register(LoginCommand())
_instance.register(PrintWorkingDirectoryCommand())
_instance.register(ListCommand())
_instance.register(ChangeDirectoryCommand())
_instance.register(LocalChangeDirectoryCommand())
_instance.register(UploadCommand())
_instance.register(DownloadCommand())
_instance.register(PlayCommand())
_instance.register(ExitCommand())
_instance.register(DebugCommand())
_instance.register(CloudTaskAddCommand())

def get_command_names():
    return _instance.get_command_names()

def parse_input(line):
    pos = line.find(' ')
    cmd_name = line if pos < 0 else line[0:pos]
    args = None if pos < 0 else line[pos+1:]
    cmd = _instance.get_command(cmd_name)
    return cmd, _split_args(args)
def _split_args(args_str):
    args = []
    tker = util.ArgumentTokenize(args_str)
    while 1:
        arg = tker.next()
        if arg is None: break
        # 去掉首尾的引号
        if arg[0] == '"' and arg[-1] == '"':
            arg = arg[1:-1]
        elif arg[0] == "'" and arg[-1] == "'":
            arg = arg[1:-1]
        args.append(arg)
    return args[0] if len(args) == 1 else args