# -*- coding: utf-8 -*-

from PIL import Image

__author__ = 'deadblue'

def convert_ascii(img_file):
    img = Image.open(img_file, 'r')
    img = img.convert('L')
    w,h = img.size
    # 生成矩阵
    martix = []
    for y in xrange(h):
        row = []
        for x in xrange(w):
            p = img.getpixel((x, y))
            row.append(0 if p > 192 else 1)
        martix.append(row)
    return _martix_to_map(_crop_and_border(martix))

def _crop_and_border(martix):
    # 统计四周空白大小
    t,b,l,r = 0,0,0,0
    for y in xrange(len(martix)):
        if sum(martix[y]) == 0:
            t += 1
        else: break
    for y in xrange(len(martix)):
        if sum(martix[-1 - y]) == 0:
            b += 1
        else: break
    for x in xrange(len(martix[0])):
        if sum( map(lambda row:row[x], martix) ) == 0:
            l += 1
        else: break
    for x in xrange(len(martix[0])):
        if sum( map(lambda row:row[-1 - x], martix) ) == 0:
            r += 1
        else: break
    # 上下裁剪与补边
    w = len(martix[0])
    if t > 0:
        martix = martix[t-1:]
    else:
        martix.insert(0, [0] * w)
    if b > 0:
        martix = martix[:1-b]
    else:
        martix.append([0] * w)
    # 左右裁剪与补边
    for ri in xrange(len(martix)):
        row = martix[ri]
        if l > 0:
            row = row[l-1:]
        else:
            row.insert(0, 0)
        if r > 0:
            row = row[:1-r]
        else:
            row.append(0)
        martix[ri] = row
    return martix

def _martix_to_map(martix):
    buf = []
    for row in martix:
        for cell in row:
            buf.append('#' if cell == 0 else ' ')
        buf.append('\n')
    return ''.join(buf)