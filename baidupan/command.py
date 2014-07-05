# -*- coding: utf-8 -*-
'''
Created on 2014/07/05

@author: deadblue
'''
from baidupan import share

__all__ = ['manager']

class Command():
    def __init__(self, name):
        self.name = name
    def execute(self, arg=None):
        pass

class LoginCommand(Command):
    def __init__(self):
        Command.__init__(self, 'login')
    def execute(self, arg=None):
        pair = arg.split(' ')
        account = pair[0]
        password = pair[1]
        share.client.login(account, password)

class ListCommand(Command):
    def __init__(self):
        Command.__init__(self, 'ls')
    def execute(self, arg=None):
        files = share.client.list(share.context.get('work_dir'))
        for fl in files['list']:
            print fl['server_filename']

class ChangeDirectoryCommand(Command):
    def __init__(self, name):
        Command.__init__(self, 'cd')
    def execute(self, arg=None):
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