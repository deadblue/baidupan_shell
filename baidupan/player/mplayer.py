# -*- coding: utf-8 -*-
'''
Created on 2014/07/11

@author: deadblue
'''

from baidupan import context
import subprocess

def play(video_req, zoom=None):
    '''
    播放视频
    @param video_req: 视频请求
    @param zoom: 缩放设置
    '''
    cmd = ['mplayer']
    # 减少输出
    cmd.append('-quiet')    # -really-quiet
    # 播放界面
    cmd.append('-osdlevel')
    cmd.append('1')
    # 优先使用IPv4
    cmd.append('-prefer-ipv4')
    # 缓冲区大小
    cmd.append('-cache')
    cmd.append('8192')
    # 缩放参数的处理
    if zoom:
        if type(zoom) is str and zoom == 'fs':
            cmd.append('-fs')
        elif type(zoom) is int:
            cmd.append('-xy')
            cmd.append(str(zoom))
        elif type(zoom) is tuple:
            cmd.append('-x')
            cmd.append(str(zoom[0]))
            cmd.append('-y')
            cmd.append(str(zoom[1]))
    # user-agent
    ua = video_req.get_header('User-Agent')
    if ua:
        cmd.append('-user-agent')
        cmd.append(ua)
    # referer
    ref = video_req.get_header('Referer')
    if ref:
        cmd.append('-referrer')
        cmd.append(ref)
    # cookie
    cmd.append('-cookies')
    cmd.append('-cookies-file')
    cmd.append(context.cookie_file)
    # 视频地址
    cmd.append(video_req.get_full_url())
    # 执行命令
    subprocess.call(cmd)
