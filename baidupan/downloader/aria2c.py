# -*- coding: utf-8 -*-
'''
Created on 2014/07/11

@author: deadblue
'''

import subprocess
import os

def download(download_req, save_path):
    cmd = ['aria2c']
    # request header
    for hdr in download_req.header_items():
        cmd.append('--header')
        cmd.append('%s: %s' % hdr)
    # save path
    save_dir, save_name = os.path.split(save_path)
    cmd.append('--dir')
    cmd.append(save_dir)
    cmd.append('--out')
    cmd.append(save_name)
    # download url
    cmd.append(download_req.get_full_url())
    # run it
    subprocess.call(cmd)