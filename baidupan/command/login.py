# -*- coding: utf-8 -*-
'''
Created on 2014/07/07

@author: deadblue
'''

from baidupan import context
from baidupan.command import Command
import getpass

class LoginCommand(Command):
    def __init__(self):
        Command.__init__(self, 'login', False)
    def execute(self, args):
        account = password = None
        if len(args) >= 1:
            account = args[0]
            if len(args) >= 2:
                password = args[1]
        if account is None:
            account = raw_input('Your account: ')
        if password is None:
            password = getpass.getpass('Your password: ')
        context.client.login(account, password)
        context.cookie_jar.save()
