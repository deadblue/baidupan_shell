#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2014/07/05

@author: deadblue
'''

import argparse
import sys

from baidupan import config

def on_exit():
    config.save()

def _main(args):
    # 使用现成的库处理传入的参数
    parser = argparse.ArgumentParser('baidupan_cli.py')
    parser.add_argument('-a', '--account')
    parser.add_argument('-p', '--password')
    parser.add_argument('-ld', '--local_dir')
    parser.add_argument('--debug', action='store_true')
    opts, args = parser.parse_known_args(args)

    from baidupan import config
    config.load()
    from baidupan import context
    context.init(opts)
    from baidupan import console
    console.run(opts)

if __name__ == '__main__':
    _main(sys.argv[1:])

