# -*- coding: utf-8 -*-
'''
Created on 2014/07/05

@author: deadblue
'''

from baidupan import context, api
from baidupan.command import manager
import readline

def completer(prefix, index):
    # 获取当前行
    #line = readline.get_line_buffer()
    # TODO: 实现自动完成
    # 需要每个命令上增加接口，暂不实现
    return None

class Console():
    def __init__(self):
        # 绑定readline
        readline.parse_and_bind('tab: complete')
        readline.set_completer(completer)
    def run(self):
        while context.alive:
            prompt = 'YunPan:%s> ' % context.get_rwd()
            # 获取输入
            line = raw_input(prompt).strip()
            # 跳过空行
            if len(line) == 0: continue
            # 解析命令和参数
            cmd, args = manager.parse_input(line)
            if cmd is None:
                print 'No such command, type help to get more info'
                continue
            if cmd.need_login and not api.client.is_login:
                print 'You MUST login before use %s' % cmd.name
                continue
            # 执行命令
            try:
                cmd.execute(args)
            except:
                print 'execute %s error!' % cmd.name
