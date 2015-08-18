# -*- coding: utf-8 -*-

from StringIO import StringIO

try:
    import Image
except:
    from PIL import Image

__author__ = 'deadblue'

def convert_ascii(img_data):
    return _matrix_to_ascii(
        _crop_and_border(
            _image_to_matrix(img_data)
        )
    )

def _image_to_matrix(img_data):
    img = Image.open(StringIO(img_data)).convert('L')
    w,h = img.size
    # 生成矩阵
    martix = []
    for y in xrange(h / 2):
        row = []
        for x in xrange(w):
            p1 = img.getpixel((x, y * 2))
            p2 = img.getpixel((x, y * 2 + 1))
            if p1 > 192 and p2 > 192:
                row.append(0)
            elif p1 > 192:
                row.append(1)
            elif p2 > 192:
                row.append(2)
            else:
                row.append(3)
        martix.append(row)
    return martix

def _crop_and_border(matrix):
    # 统计四周空白大小
    t,b,l,r = 0,0,0,0
    for y in xrange(len(matrix)):
        if sum(matrix[y]) == 0:
            t += 1
        else: break
    for y in xrange(len(matrix)):
        if sum(matrix[-1 - y]) == 0:
            b += 1
        else: break
    for x in xrange(len(matrix[0])):
        if sum( map(lambda row:row[x], matrix) ) == 0:
            l += 1
        else: break
    for x in xrange(len(matrix[0])):
        if sum( map(lambda row:row[-1 - x], matrix) ) == 0:
            r += 1
        else: break
    # 上下裁剪与补边
    w = len(matrix[0])
    if t > 0:
        matrix = matrix[t-1:]
    else:
        matrix.insert(0, [0] * w)
    if b > 1:
        matrix = matrix[:1-b]
    elif b == 0:
        matrix.append([0] * w)
    # 左右裁剪与补边
    for ri in xrange(len(matrix)):
        row = matrix[ri]
        if l > 0:
            row = row[l-1:]
        else:
            row.insert(0, 0)
        if r > 1:
            row = row[:1-r]
        elif r == 0:
            row.append(0)
        matrix[ri] = row
    return matrix

def _matrix_to_ascii(matrix):
    buf = []
    for row in matrix:
        rbuf = []
        for cell in row:
            if cell == 0:
                rbuf.append('#')
            elif cell == 1:
                rbuf.append('"')
            elif cell == 2:
                rbuf.append(',')
            elif cell == 3:
                rbuf.append(' ')
        buf.append(''.join(rbuf))
    return '\n'.join(buf)