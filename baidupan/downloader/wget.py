# -*- coding: utf-8 -*-
'''
wget下载器
Created on 2014/07/11

@author: deadblue
'''

from baidupan import util

def download(download_req, save_path):
    cmd = ['wget']
    for hdr in download_req.header_items():
        cmd.append('--header')
        cmd.append('%s: %s' % hdr)
    # download url
    cmd.append(download_req.get_full_url())
    # save_path
    cmd.extend(['-O', save_path])
    # run it
    return util.subprocess_call(cmd)