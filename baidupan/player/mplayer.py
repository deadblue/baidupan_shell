# -*- coding: utf-8 -*-
'''
Created on 2014/07/11

@author: deadblue
'''

from baidupan import context, util

def play(video_req, zoom=None):
    '''
    播放视频
    @param video_req: 视频请求
    @param zoom: 缩放设置
    '''
    cmd = ['mplayer',
           '-quiet',            # 减少输出
           '-osdlevel', '1',    # 界面选项
           '-prefer-ipv4',      # 优先使用IPv4
           '-cache', '8192']    # 缓冲区大小
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
    ua = video_req.get_header('User-agent') # 取出header时只有首字母大写
    if ua:
        cmd.append('-user-agent')
        cmd.append(ua)
    # referer
    ref = video_req.get_header('Referer')
    if ref:
        cmd.append('-referrer')
        cmd.append(ref)
    # cookie
    cmd.extend(['-cookies', '-cookies-file', context.cookie_file])
    # 视频地址
    cmd.append(video_req.get_full_url())
    # 执行命令
    return util.subprocess_call(cmd)