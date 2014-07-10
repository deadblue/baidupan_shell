# -*- coding: utf-8 -*-
'''
Created on 2014/07/10

@author: deadblue
'''

from baidupan.command import Command
from baidupan import context

class PlayCommand(Command):
    def __init__(self):
        Command.__init__(self, 'play', True)
    def execute(self, file_id):
        file_id = int(file_id)
        context.client.play(file_id)