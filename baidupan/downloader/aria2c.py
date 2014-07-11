# -*- coding: utf-8 -*-
'''
Created on 2014/07/11

@author: deadblue
'''

from baidupan import context
import subprocess
import os

def download(file_req, save_path):
    cmd = ['aria2c']
    # user-agent
    ua = file_req.get_header('User-Agent')
    if ua: cmd.append('--user-agent=%s' % ua)
    # referer
    ref = file_req.get_header('Referer')
    if ref: cmd.append('--referer=%s"' % ref)
    # cookie
    cmd.append('--load-cookies')
    cmd.append(context.cookie_file)
    # save path
    save_dir, save_name = os.path.split(save_path)
    cmd.append('--dir')
    cmd.append(save_dir)
    cmd.append('--out')
    cmd.append(save_name)
    # download url
    cmd.append(file_req.get_full_url())
    # run it
    subprocess.call(cmd)