# -*- coding: utf-8 -*-
'''
Created on 2014/07/11

@author: deadblue
'''

from baidupan import util

def download(download_req, save_path):
    cmd = ['curl', '-L']
    # request header
    for hdr in download_req.header_items():
        cmd.append('-H')
        cmd.append('%s: %s' % hdr)
    # save path
    cmd.extend(['--output', save_path])
    # download url
    cmd.append(download_req.get_full_url())
    # run it!
    return util.subprocess_call(cmd)