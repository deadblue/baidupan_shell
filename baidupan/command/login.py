# -*- coding: utf-8 -*-
'''
Created on 2014/07/07

@author: deadblue
'''

from baidupan import context
from baidupan.command import Command, InvalidArgumentException

class LoginCommand(Command):
    def __init__(self):
        Command.__init__(self, 'login', False)
    def execute(self, arg=None):
        account, password = self._parse_arg(arg)
        context.client.login(account, password)
        context.cookie_jar.save()
    def _parse_arg(self, arg):
        if arg is None:
            raise InvalidArgumentException()
        pair = arg.split(' ')
        if len(pair) < 2:
            raise InvalidArgumentException()
        return pair[0], pair[1]
