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

class ArgumentTokenizer(object):
    def __init__(self, line):
        self._raw = line
        self._raw_length = 0 if line is None else len(line)
        self._pointer = 0
    def next(self):
        if self._raw is None:
            return
        if self._pointer >= self._raw_length:
            return
        buf = []
        while self._pointer < self._raw_length:
            ch = self._raw[self._pointer]
            self._pointer += 1
            if len(buf) == 0:
                if ch != ' ': buf.append(ch)
            else:
                if self._is_token_stop(buf, ch): break
                else: buf.append(ch)
        return self._escape_and_join(buf)
    def _is_token_stop(self, buf, ch):
        return ch == ' ' and buf[-1] != '\\' and self._is_quote_close(buf)
    def _is_quote_close(self, buf):
        quote_count = 0
        for ch in buf:
            if ch == '"':
                quote_count += 1
        return quote_count % 2 == 0
    def _escape_and_join(self, buf):
        if buf[0] == '"' and buf[-1] == '"':
            buf = buf[1:-1]
        for i in xrange(len(buf) - 1, 0, -1):
            if buf[i] == ' ':
                if i > 0 and buf[i-1] == '\\':
                    del buf[i - 1]
                    i -= 2
        return ''.join(buf)