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
    def execute(self, args):
        if len(args) == 0:
            print 'nothing to play!'
        else:
            file_id = args[0]
            video_req = context.client.get_download_request(int(file_id))
            if type(video_req) is list and len(video_req) == 0:
                print 'No such file!'
            else:
                mplayer.play(video_req, 848)
