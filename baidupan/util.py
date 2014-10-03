# -*- coding: utf-8 -*-
'''
Created on 2014/07/05

@author: deadblue
'''

import random
import time
import os

def get_data_file(data_name):
    data_path = os.getenv('HOME') or os.getenv('USERPROFILE')
    return os.path.join(data_path, data_name)
    
def timstamp():
    return int(time.time() * 1000)

def format_time(seconds):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(seconds))

def format_size(size):
    if size > 1073741824:
        size /= 1073741824.0
        return '%.2f GB' % size
    elif size > 1048576:
        size /= 1048576.0
        return '%.2f MB' % size
    elif size > 1024:
        size /= 1024.0
        return '%.2f KB' % size
    else:
        return str(size)

def random_hex_str(length=6):
    source = '0123456789abcdef'
    return random_str(source, length)

def random_str(source, length):
    buf = []
    for _ in xrange(0, length):
        buf.append(random.choice(source))
    return ''.join(buf)

def encode_utf8(s):
    return s.encode('utf-8') if type(s) is unicode else s

def default_vcode_handler(img_data):
    import tempfile
    _, tmp_file_path = tempfile.mkstemp(suffix='.jpg')
    with open(tmp_file_path, 'wb') as fp:
        fp.write(img_data)
    print 'vcode image saved to: %s' % tmp_file_path
    return raw_input('Verification code: ')

def ascii_vcode_handler(img_data):
    # 将验证码转换成ascii并输出到终端
    from baidupan import vcode
    print vcode.convert_ascii(img_data)
    # 提示用户输入看到的验证码
    return raw_input('The CODE you see above: ')

def parser_arguments(argv):
    arg_map = {}
    arg_name = None
    for arg in argv:
        if arg.startswith('-'):
            # 以-开头表示参数名
            if arg_name and not arg_map.has_key(arg_name):
                arg_map[arg_name] = True
            arg_name = arg[1:]
        else:
            # 否则为参数值
            if arg_name is None: continue
            if arg_map.has_key(arg_name):
                arg_val = arg_map[arg_name]
                if type(arg_val) is list:
                    arg_val.append(arg)
                else:
                    arg_val = [arg_val, arg]
                    arg_map[arg_name] = arg_val
            else:
                arg_map[arg_name] = arg
    # 最终处理
    if arg_name and not arg_map.has_key(arg_name):
        arg_map[arg_name] = True
    return arg_map

def escape_arg(arg):
    return arg.replace('\\ ', ' ')

def unescape_arg(arg):
    return arg.replace(' ', '\\ ')

def subprocess_call(args):
    # 对参数组中的unicode字符串进行编码
    import locale
    encoding = locale.getpreferredencoding()
    for i in xrange(len(args)):
        if type(args[i]) is unicode:
            args[i] = args[i].encode(encoding)
    # 创建子进程
    import subprocess
    return subprocess.call(args)