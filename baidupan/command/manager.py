# -*- coding: utf-8 -*-
'''
Created on 2014/07/07

@author: deadblue
'''

class _Manager():
    def __init__(self):
        self._commands = {}
    def register(self, cmd):
        self._commands[cmd.name] = cmd
    def get_command(self, name):
        return self._commands[name] if self._commands.has_key(name) else None

_instance = _Manager()

def register(cmd):
    _instance.register(cmd)

def get_command(name):
    return _instance.get_command(name)