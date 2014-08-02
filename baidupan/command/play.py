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
        if type(file_id) is list: file_id = file_id[0]
        file_id = int(file_id)
        video_req = context.client.get_download_request(file_id)
        if type(video_req) is list and len(video_req):
            print 'No such file!'
        else:
            mplayer.play(video_req, 848)
