# -*- coding: utf-8 -*-
'''
Created on 2014/07/07

@author: deadblue
'''

from baidupan import util
from baidupan.command.cd import ChangeDirectoryCommand
from baidupan.command.dl import CloudDownloadCommand
from baidupan.command.conf import ConfigCommand
from baidupan.command.debug import DebugCommand
from baidupan.command.exit import ExitCommand
from baidupan.command.lcd import LocalChangeDirectoryCommand
from baidupan.command.login import LoginCommand
from baidupan.command.ls import ListCommand
from baidupan.command.play import PlayCommand
from baidupan.command.pull import PullCommand
from baidupan.command.push import PushCommand
from baidupan.command.pwd import PrintWorkingDirectoryCommand
from baidupan.command.rm import RemoveCommand
from baidupan.command.tasks import TaskListCommand

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
_instance.register(ChangeDirectoryCommand())
_instance.register(LocalChangeDirectoryCommand())
_instance.register(ListCommand())
_instance.register(RemoveCommand())
_instance.register(PushCommand())
_instance.register(PullCommand())
_instance.register(PlayCommand())
_instance.register(TaskListCommand())
_instance.register(CloudDownloadCommand())
_instance.register(ExitCommand())
_instance.register(DebugCommand())

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
    tker = util.ArgumentTokenizer(args_str)
    while 1:
        arg = tker.next()
        if arg is None: break
        args.append(arg)
    return args[0] if len(args) == 1 else args