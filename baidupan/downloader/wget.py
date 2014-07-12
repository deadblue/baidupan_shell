# -*- coding: utf-8 -*-
'''
wget下载器，传cookie有问题，待修正
Created on 2014/07/11

@author: deadblue
'''

import subprocess

def download(download_req, save_path):
    cmd = ['wget']
    for hdr in download_req.header_items():
        cmd.append('--header')
        cmd.append('%s: %s' % hdr)
    # download url
    cmd.append(download_req.get_full_url())
    # save_path
    cmd.append('-O')
    cmd.append(save_path)
    # execute it
    subprocess.call(cmd)