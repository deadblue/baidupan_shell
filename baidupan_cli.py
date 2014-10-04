#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2014/07/05

@author: deadblue
'''

from baidupan import config, context, usage

def on_exit():
    config.save()

if __name__ == '__main__':
    # 参数处理
    args = usage.parse_arguments()
    if args.get('help'):
        usage.print_usage()
    else:
        import atexit
        atexit.register(on_exit)
        # 加载配置
        config.load()
        # 初始化运行环境
        context.init(args)
        # 启动文字终端
        from baidupan import console
        console.run(args)
