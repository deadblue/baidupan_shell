#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2014/07/05

@author: deadblue
'''

from baidupan import config, context
import atexit

def on_exit():
    context.log_file.close()
    config.save()

if __name__ == '__main__':
    atexit.register(on_exit)
    config.load()
    context.init()

    from baidupan import console
    console.run()
