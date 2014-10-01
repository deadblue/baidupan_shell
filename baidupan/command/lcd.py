# -*- coding: utf-8 -*-
'''
Created on 2014/07/07

@author: deadblue
'''

import logging
import os

from baidupan import context, tree
from baidupan.command import Command

_logger = logging.getLogger('lcd')

class LocalChangeDirectoryCommand(Command):
    def __init__(self):
        Command.__init__(self, 'lcd', False)
    def execute(self, args=[]):
        target_dir = args[0] if len(args) > 0 else ''
        lwd = context.get_lwd()
        if tree.local_isabspath(target_dir):
            lwd = target_dir
        else:
            lwd = os.path.join(lwd, target_dir)
        lwd = tree.local_abspath(lwd)
        if not lwd.endswith(os.sep):
            lwd += os.sep
        context.set_lwd(lwd)

    def get_completer_words(self, target_dir):
        if not tree.local_isabspath(target_dir):
            target_dir = os.path.join(context.get_lwd(), target_dir)
        parent_dir, prefix = tree.local_splitpath(target_dir)
        sub_dirs = filter(lambda x:len(prefix) == 0 or x.startswith(prefix),
                          tree.local_listdir(parent_dir))
        _logger.debug(sub_dirs)
        return map(lambda x:'%s%s' % (x,os.sep), sub_dirs)