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
    for arg in args:
        if arg.startswith('--'):
            arg_name = arg[2:]
            eq_pos = arg_name.find('=')
            if eq_pos >= 0:
                arg_value = arg_name[eq_pos + 1:]
                arg_name = arg_name[0:eq_pos]
            else:
                arg_value = True
        elif arg.startswith('-'):
            arg_name = arg[1:]
            eq_pos = arg_name.find('=')
            if eq_pos >= 0:
                arg_value = arg_name[eq_pos + 1:]
                arg_name = arg_name[0:eq_pos]
            else:
                arg_value = True
            arg_name = _get_fullname(arg_name)
        if arg_name is None: continue
        arg_dict[arg_name] = arg_value
    return arg_dict

def print_usage():
    print 'Usage: %s [options]' % sys.argv[0]
    print 'Options:'
    def _format(info):
        form = None
        if info[2]:
            form = '-%s, --%s=<%s>' % (info[0], info[1], info[2])
        else:
            form = '-%s, --%s' % (info[0], info[1])
        return '  %-33s%s' % (form, info[3])
    print '\n'.join(map(_format, _USAGE))
