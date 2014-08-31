# -*- coding: utf-8 -*-

__author__ = 'deadblue'

def remote_abspath(full_path):
    if full_path is None:
        return '/'
    dirs = full_path.split('/')
    seps = []
    for d in dirs:
        if d == '.': continue
        if d == '..':
            if len(seps) > 1: seps.pop()
            else: continue
        else:
            seps.append(d)
    return '/'.join(seps)