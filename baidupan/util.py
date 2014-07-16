# -*- coding: utf-8 -*-
'''
Created on 2014/07/05

@author: deadblue
'''

import random
import time
import os

def get_data_file(data_name):
    data_path = os.getenv('HOME') or os.getenv('USERPROFILE')
    return os.path.join(data_path, data_name)
    
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

class ArgumentTokenize(object):
    def __init__(self, raw_args):
        self._raw = raw_args
        self._pointer = 0
    def next(self):
        if self._raw is None:
            return None
        if self._pointer >= len(self._raw):
            return None
        buf = []
        quote = None
        while self._pointer < len(self._raw):
            ch = self._raw[self._pointer]
            self._pointer += 1
            if ch == ' ' and quote is None:
                if len(buf) > 0: break
                else: continue
            elif ch == '"' or ch == "'":
                if quote is None: quote = ch
                elif quote == ch: quote = None
            buf.append(ch)
        return ''.join(buf) if len(buf) > 0 else None
