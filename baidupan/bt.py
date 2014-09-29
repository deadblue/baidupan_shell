# -*- coding: utf-8 -*-

__author__ = 'deadblue'

import time
import bencode

def mask(torrent_data):
    '''
    混淆种子内容
    :param torrent_data: 种子文件内容
    :return: (混淆后的种子文件内容,混淆字典)
    '''
    name_dict = _mask_filename(torrent_data)
    torrent_data = bencode.bencode(torrent_data)
    return torrent_data, name_dict

def mask_file(torrent_file):
    '''
    混淆种子文件
    :param torrent_file: 种子文件
    :return: (混淆后的种子文件内容,混淆字典)
    '''
    with open(torrent_file, 'r') as fp:
        torrent_data = bencode.bdecode(fp.read())
    return mask(torrent_data)

def _mask_filename(torrent_data):
    # 初始化字典
    name_dict = {
        'version' : '1.0',
        'prefix' : '%x' % time.time(),
        'names' : []
    }
    def get_mask_name(name):
        index = -1
        names = name_dict['names']
        if name in names:
            index = names.index(name) + 1
        else:
            names.append(name)
            index = len(names)
        return '%s_%d' % (name_dict['prefix'], index)
    # 解码处理
    encoding = torrent_data.get('encoding')
    def decode_name(name):
        return name.decode(encoding) if encoding else name
    # 处理种子信息
    torrent_info = torrent_data['info']
    # 替换主名称
    main_name = decode_name(torrent_info['name'])
    replace_name = get_mask_name(main_name)
    torrent_info['name'] = replace_name
    if torrent_info.has_key('name.utf-8'):
        torrent_info['name.utf-8'] = replace_name
    # 若包含子文件，替换子文件名称
    if torrent_info.has_key('files'):
        for file_info in torrent_info['files']:
            # 跳过BitComit添加的无用文件
            if file_info['path'][0].startswith('_____padding_file_'): continue
            # 路径处理
            for i in xrange(len(file_info['path'])):
                path_name = decode_name(file_info['path'][i])
                replace_name = get_mask_name(path_name)
                file_info['path'][i] = replace_name
            if file_info.has_key('path.utf-8'):
                file_info['path.utf-8'] = file_info['path']
    return name_dict