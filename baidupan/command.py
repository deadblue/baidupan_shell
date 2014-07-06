# -*- coding: utf-8 -*-
'''
Created on 2014/07/05

@author: deadblue
'''

from baidupan import api, context

__all__ = ['manager', 'InvalidArgumentException']

class InvalidArgumentException(Exception):
    pass

class Command():
    def __init__(self, name):
        self.name = name
    def execute(self, arg=None):
        pass

class LoginCommand(Command):
    def __init__(self):
        Command.__init__(self, 'login')
    def execute(self, arg=None):
        account, password = self._parse_arg(arg)
        api.client.login(account, password)
    def _parse_arg(self, arg):
        if arg is None:
            raise InvalidArgumentException()
        pair = arg.split(' ')
        if len(pair) < 2:
            raise InvalidArgumentException()
        return pair[0], pair[1]

class ListCommand(Command):
    def __init__(self):
        Command.__init__(self, 'ls')
    def execute(self, arg=None):
        files = api.client.list(context.get(context.PWD))
        print '%-20s %-16s %s' % ('file_id', 'size', 'name')
        for fl in files['list']:
            print '%-20d %-16d %s' % (fl['fs_id'], fl['size'], fl['server_filename'])

class ChangeDirectoryCommand(Command):
    def __init__(self):
        Command.__init__(self, 'cd')
    def execute(self, arg=None):
        # TODO: 处理各种相对路径
        pwd = context.get(context.PWD)
        pwd = '%s%s/' % (pwd, arg)
        context.put(context.PWD, pwd)

class LocalChangeDirectoryCommand(Command):
    def __init__(self):
        Command.__init__(self, 'lcd')
    def execute(self, arg=None):
        if arg is None:
            raise InvalidArgumentException()
        context.put(context.LWD, arg)

class MakeDirectoryCommand(Command):
    def __init__(self):
        Command.__init__(self, 'mkdir')
    def execute(self, arg=None):
        # TODO: 实现创建目录
        pass

class RemoveFileCommand(Command):
    def __init__(self):
        Command.__init__(self, 'rm')
    def execute(self, arg=None):
        files = self._parse_arg(arg)
        api.client.delete_files(files)
    def _parse_arg(self, arg):
        # TODO: 拆分函数
        pass

class CommandManager():
    def __init__(self):
        self._commands = {}
    def register(self, cmd):
        self._commands[cmd.name] = cmd
    def get_command(self, name):
        return self._commands[name] if self._commands.has_key(name) else None

manager = CommandManager()
manager.register(LoginCommand())
manager.register(ListCommand())
manager.register(ChangeDirectoryCommand())
manager.register(RemoveFileCommand())