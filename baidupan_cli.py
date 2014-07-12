#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2014/07/05

@author: deadblue
'''

from baidupan import config, console
import atexit

def on_exit():
    config.save()

if __name__ == '__main__':
    atexit.register(on_exit)
    config.load()
    console.run()
