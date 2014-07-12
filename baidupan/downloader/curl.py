# -*- coding: utf-8 -*-
'''
Created on 2014/07/11

@author: deadblue
'''

import subprocess

def download(download_req, save_path):
    cmd = ['curl']
    # auto redirect
    cmd.append('-L')
    # request header
    for hdr in download_req.header_items():
        cmd.append('-H')
        cmd.append('%s: %s' % hdr)
    # compressed date
    cmd.append('--compressed')
    # save path
    cmd.append('--output')
    cmd.append(save_path)
    # download url
    cmd.append(download_req.get_full_url())
    # run it!
    subprocess.call(cmd)
