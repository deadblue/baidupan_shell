# -*- coding: utf-8 -*-
'''
Created on 2014/07/07

@author: deadblue
'''

# 命令列表
_command_dict = {}

def init():
    # 注册命令
    def _register_command(cmd):
        _command_dict[cmd.name] = cmd
    from baidupan.command.conf import ConfigCommand
    _register_command(ConfigCommand())
    from baidupan.command.login import LoginCommand
    _register_command(LoginCommand())
    from baidupan.command.pwd import PrintWorkingDirectoryCommand
    _register_command(PrintWorkingDirectoryCommand())
    from baidupan.command.cd import ChangeDirectoryCommand
    _register_command(ChangeDirectoryCommand())
    from baidupan.command.lcd import LocalChangeDirectoryCommand
    _register_command(LocalChangeDirectoryCommand())
    from baidupan.command.ls import ListCommand
    _register_command(ListCommand())
    from baidupan.command.mkdir import CreateDirectoryCommand
    _register_command(CreateDirectoryCommand())
    from baidupan.command.rm import RemoveCommand
    _register_command(RemoveCommand())
    from baidupan.command.push import PushCommand
    _register_command(PushCommand())
    from baidupan.command.pull import PullCommand
    _register_command(PullCommand())
    from baidupan.command.play import PlayCommand
    _register_command(PlayCommand())
    from baidupan.command.tasks import TaskListCommand
    _register_command(TaskListCommand())
    from baidupan.command.dl import CloudDownloadCommand
    _register_command(CloudDownloadCommand())
    from baidupan.command.unmask import UnmaskCommand
    _register_command(UnmaskCommand())
    from baidupan.command.exit import ExitCommand
    _register_command(ExitCommand())

def get_command_names():
    return _command_dict.keys()

def get_command(name):
    return _command_dict.get(name)

def parse_input(line):
    pos = line.find(' ')
    cmd_name = line if pos < 0 else line[0:pos]
    args = None if pos < 0 else line[pos+1:]
    cmd = get_command(cmd_name)
    return cmd, _split_args(args)
def _split_args(args_str):
    args = []
    tker = _CommandArgumentTokenizer(args_str)
    while 1:
        arg = tker.next()
        if arg is None: break
        args.append(arg)
    return args
class _CommandArgumentTokenizer(object):
    def __init__(self, line):
        self._raw = line
        self._raw_length = 0 if line is None else len(line)
        self._pointer = 0
    def next(self):
        if self._raw is None:
            return
        if self._pointer >= self._raw_length:
            return
        buf = []
        while self._pointer < self._raw_length:
            ch = self._raw[self._pointer]
            self._pointer += 1
            if len(buf) == 0:
                if ch != ' ': buf.append(ch)
            else:
                if self._is_token_stop(buf, ch): break
                else: buf.append(ch)
        return self._escape_and_join(buf)
    def _is_token_stop(self, buf, ch):
        return ch == ' ' and buf[-1] != '\\' and self._is_quote_close(buf)
    def _is_quote_close(self, buf):
        quote_count = 0
        for ch in buf:
            if ch == '"':
                quote_count += 1
        return quote_count % 2 == 0
    def _escape_and_join(self, buf):
        if buf[0] == '"' and buf[-1] == '"':
            buf = buf[1:-1]
        return ''.join(buf).replace('\\ ', ' ')