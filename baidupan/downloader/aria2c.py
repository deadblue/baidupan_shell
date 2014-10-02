# -*- coding: utf-8 -*-
'''
Created on 2014/07/11

@author: deadblue
'''

import os

from baidupan import util

def download(download_req, save_path):
    # build command
    cmd = ['aria2c', '--file-allocation=none']
    # request header
    for hdr in download_req.header_items():
        cmd.append('--header')
        cmd.append('%s: %s' % hdr)
    # save path
    save_dir, save_name = os.path.split(save_path)
    cmd.extend(['--dir', save_dir, '--out', save_name])
    # download url
    cmd.append(download_req.get_full_url())
    # run it
    return util.subprocess_call(cmd)