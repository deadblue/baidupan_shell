# -*- coding: utf-8 -*-
'''
wget下载器，传cookie有问题，待修正
Created on 2014/07/11

@author: deadblue
'''

import subprocess
from baidupan import context

def download(file_req, save_path):
    cmd = ['wget']
    # user-agent
    ua = file_req.get_header('User-Agent')
    if ua: cmd.append('--user-agent="%s"' % ua)
    # referer
    ref = file_req.get_header('Referer')
    if ref: cmd.append('--referer="%s"' % ref)
    # cookie
    cmd.append('--load-cookies')
    cmd.append(context.cookie_file)
    # download url
    cmd.append(file_req.get_full_url())
    # save_path
    cmd.append('-O')
    cmd.append(save_path)
    print cmd
    # execute it
    subprocess.call(cmd)