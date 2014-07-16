# -*- coding: utf-8 -*-
'''
Created on 2014/07/13

@author: deadblue
'''

from baidupan.command import Command
from baidupan import config

class ConfigCommand(Command):
    def __init__(self):
        Command.__init__(self, 'conf', False)
    def execute(self, args=None):
        if len(args) == 0:
            conf_data = config.get_all()
            for pair in conf_data.items():
                print '%s => %r' % pair
        elif len(args) == 1:
            print config.get(args[0])
        else:
            config.put(args[0], ' '.join(args[1:]))
