# -*- coding: utf-8 -*-
'''
Created on 2014/07/11

@author: deadblue
'''

import locale
import os
import subprocess

def download(download_req, save_path):
    # select encoding
    encoding = locale.getpreferredencoding()
    # build command
    cmd = ['aria2c', '--file-allocation=none']
    # request header
    for hdr in download_req.header_items():
        cmd.append('--header')
        cmd.append('%s: %s' % hdr)
    # save path
    save_dir, save_name = os.path.split(save_path.encode(encoding))
    cmd.extend(['--dir', save_dir, '--out', save_name])
    # download url
    cmd.append(download_req.get_full_url().encode(encoding))
    # run it
    subprocess.call(cmd)