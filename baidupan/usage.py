# -*- coding: utf-8 -*-

import sys

__author__ = 'deadblue'

# format: (shortname, fullname, value, description)
_USAGE = [
    ('h', 'help', None, 'Show usage only'),
    ('a', 'account', 'account', 'Login by account'),
    ('p', 'password', 'password', 'Login password for account'),
    ('c', 'cookie', 'cookie-file-path', 'Specity a cookie file'),
    ('l', 'local', 'local-dir-path', 'Default local work directory'),
    ('d', 'debug', None, 'Run in debug mode'),
]
def _get_fullname(shortname):
    for sn, fn, _, _ in _USAGE:
        if sn == shortname: return fn
    return None

def parse_arguments(args=sys.argv[1:]):
    arg_dict = {}
    last_arg_name = None
    for arg in args:
        if arg.startswith('-'):
            if arg.startswith('--'):
                arg_name = arg[2:]
            else:
                arg_name = arg[1:]
                arg_name = _get_fullname(arg_name)
            last_arg_name = arg_name
            arg_dict[arg_name] = True
        else:
            if last_arg_name is None: continue
            arg_dict[last_arg_name] = arg
            last_arg_name = None
    return arg_dict

def print_usage():
    print 'Usage: %s [options]' % sys.argv[0]
    print 'Options:'
    def _format(info):
        form = None
        if info[2]:
            form = '-%s, --%s <%s>' % (info[0], info[1], info[2])
        else:
            form = '-%s, --%s' % (info[0], info[1])
        return '  %-33s%s' % (form, info[3])
    print '\n'.join(map(_format, _USAGE))