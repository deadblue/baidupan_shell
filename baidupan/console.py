# -*- coding: utf-8 -*-
'''
Created on 2014/07/05

@author: deadblue
'''

from baidupan import command

class Console():
    def __init__(self):
        pass
    def run(self):
        while 1:
            line = raw_input('/ > ')
            if line == 'exit':
                break
            else:
                pos = line.find(' ')
                cmd = line if pos < 0 else line[0:pos]
                cmd = command.manager.get_command(cmd)
                if cmd:
                    cmd.execute()
                else:
                    print 'invalid command'
        print 'baidupan_cli exit!'
