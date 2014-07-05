#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2014/07/05

@author: deadblue
'''

from baidupan.console import Console
import atexit

def on_exit():
    pass

if __name__ == '__main__':
    atexit.register(on_exit)
    Console().run()
