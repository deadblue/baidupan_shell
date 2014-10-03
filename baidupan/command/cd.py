# -*- coding: utf-8 -*-
'''
Created on 2014/07/07

@author: deadblue
'''

from baidupan import context, tree, util
from baidupan.command import Command

class ChangeDirectoryCommand(Command):
    def __init__(self):
        Command.__init__(self, 'cd', True)

    def execute(self, args):
        target_dir = args[0] if len(args) > 0 else '/'
        if target_dir.startswith('/'):
            rwd = target_dir
        else:
            rwd = '%s%s' % (context.get_rwd(), target_dir)
        rwd = tree.remote_abspath(rwd)
        if not rwd.endswith('/'): rwd += '/'
        if context.remote_tree.dir_exists(rwd):
            context.set_rwd(rwd)
        else:
            print 'no such dir!'

    def get_completer_words(self, prefix):
        if prefix.startswith('/'):
            target_path = prefix
        else:
            target_path = '%s%s' % (context.get_rwd(), prefix)
        target_path = tree.remote_abspath(target_path)
        parent_dir, name_prefix = tree.remote_splitpath(target_path)
        dirs = context.remote_tree.list_dir(parent_dir)
        dir_names = map(lambda x:'%s/' % util.unescape_arg(x['server_filename']), dirs)
        return filter(lambda x:len(name_prefix)==0 or x.startswith(name_prefix), dir_names)