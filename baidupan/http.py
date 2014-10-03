# -*- coding: utf-8 -*-
'''
Created on 2014/07/04

@author: deadblue
'''

import string
import urllib2
import os

__all__ = ['StringPart', 'FilePart', 'FileDataPart', 'MultipartRequest']

def _create_boundary():
    import random
    buf = ['----']
    for _ in xrange(16):
        buf.append(random.choice(string.ascii_letters))
    return ''.join(buf)

def _join(array):
    for i in xrange(len(array)):
        if type(array[i]) is unicode:
            array[i] = array[i].encode('utf-8')
    return ''.join(array)

class Part():
    def __init__(self, name):
        self.name = name
    def get_data(self):
        return None

class StringPart(Part):
    def __init__(self, name, value):
        Part.__init__(self, name)
        self.value = value
    def get_data(self):
        return 'Content-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % (self.name, self.value)

class FilePart(Part):
    def __init__(self, name, filename):
        Part.__init__(self, name)
        # 读取文件内容
        fp = open(filename, 'r')
        self.filedata = fp.read()
        fp.close()
        # 文件名
        self.filename = os.path.basename(filename)
    def get_data(self):
        buf = ['Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (self.name, self.filename),
               'Content-Type: application/octet-stream\r\n\r\n', self.filedata, '\r\n']
        return _join(buf)

class FileDataPart(Part):
    def __init__(self, name, filename, filedata):
        Part.__init__(self, name)
        self.filename = filename
        self.filedata = filedata
    def get_data(self):
        buf = ['Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (self.name, self.filename),
               'Content-Type: application/octet-stream\r\n\r\n', self.filedata, '\r\n']
        return _join(buf)

class MultipartRequest(urllib2.Request):
    def __init__(self, url, headers={}):
        urllib2.Request.__init__(self, url, headers=headers)
        self.boundary = _create_boundary()
        self.headers['Content-Type'] = 'multipart/form-data; boundary=%s' % self.boundary
    def set_parts(self, parts):
        if len(parts) == 0: return
        buf = []
        for part in parts:
            buf.append('--%s\r\n' % self.boundary)
            buf.append(part.get_data())
        buf.append('--%s--\r\n' % self.boundary)
        self.data = _join(buf)

if __name__ == '__main__':
    print _create_boundary()