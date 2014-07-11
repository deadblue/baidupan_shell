# -*- coding: utf-8 -*-
'''
Created on 2014/07/10

@author: deadblue
'''

from baidupan import context
from baidupan.command import Command
from baidupan.player import mplayer

class PlayCommand(Command):
    def __init__(self):
        Command.__init__(self, 'play', True)
    def execute(self, file_id):
        file_id = int(file_id)
        video_req = context.client.get_download_request(file_id)
        mplayer.play(video_req, 848)