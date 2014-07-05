# -*- coding: utf-8 -*-
'''
Created on 2014/07/05

@author: deadblue
'''

class Console():
    def __init__(self):
        pass
    def run(self):
        while 1:
            line = raw_input('/> ')
            if line == 'exit':
                break
        print 'baidupan_cli exit!'
