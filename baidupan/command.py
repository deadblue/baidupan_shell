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
    def execute(self, arg):
        pass

class LoginCommand(Command):
    def __init__(self):
        Command.__init__(self, 'login')
    def execute(self, arg):
        pair = arg.split(' ')
        account = pair[0]
        password = pair[1]
        share.client.login(account, password)

class CommandManager():
    def __init__(self):
        self._commands = {}
    def register(self, cmd):
        self._commands[cmd.name] = cmd
    def get_command(self, name):
        return self._commands[name] if self._commands.has_key(name) else None

manager = CommandManager()
manager.register(LoginCommand())