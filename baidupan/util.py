# -*- coding: utf-8 -*-
'''
Created on 2014/07/05

@author: deadblue
'''

import random
import time

def timstamp():
    return int(time.time() * 1000)

def random_str(length=6):
    source = '0123456789abcdef'
    buf = []
    for _ in xrange(0, length):
        buf.append(random.choice(source))
    return ''.join(buf)
