# -*- coding: utf-8 -*-
'''
Created on 2014/07/05

@author: deadblue
'''

import random
import time

def timstamp():
    return int(time.time() * 1000)

def format_time(seconds):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(seconds))

def format_size(size):
    if size > 1073741824:
        size /= 1073741824.0
        return '%.2f GB' % size
    elif size > 1048576:
        size /= 1048576.0
        return '%.2f MB' % size
    elif size > 1024:
        size /= 1024.0
        return '%.2f KB' % size
    else:
        return str(size)

def random_hex_str(length=6):
    source = '0123456789abcdef'
    return random_str(source, length)

def random_str(source, length):
    buf = []
    for _ in xrange(0, length):
        buf.append(random.choice(source))
    return ''.join(buf)