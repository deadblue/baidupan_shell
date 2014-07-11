# -*- coding: utf-8 -*-
'''
Created on 2014/07/11

@author: deadblue
'''

from baidupan import context
import subprocess

def download(file_req, save_path):
    cmd = ['curl']
    cmd.append('-L')
    # user-agent
    ua = file_req.get_header('User-Agent')
    if ua:
        cmd.append('--user-agent')
        cmd.append(ua)
    # referer
    ref = file_req.get_header('Referer')
    if ref:
        cmd.append('--referer')
        cmd.append(ref)
    # cookie
    cmd.append('--cookie')
    cmd.append(context.cookie_file)
    # save_path
    cmd.append('--output')
    cmd.append(save_path)
    # download url
    cmd.append('--url')
    cmd.append(file_req.get_full_url())
    # execute it
    subprocess.call(cmd)