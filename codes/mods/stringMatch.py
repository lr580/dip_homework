import cv2
import os
from templatePredeal import strname
from toBinary import getBinary
from stringSplit import splitNumbers


def loadTemplates(path='../templates'):
    '''从文件夹路径返回标准字符模板(经过二值化)'''
    t = [dict() for i in range(3)]
    for i in range(2):
        for j in strname:
            name = '%d_%s.png' % (5+i, j)
            dest = os.path.join(path, name)
            t[i][j] = cv2.imread(dest)
            t[i][j] = getBinary(t[i][j])
    return t


tems = loadTemplates(r'D:\_lr580\program\practice\cv_homework\codes\template')


def compare(target, std):
    '''比较target与模板图像std的相似性并返回'''
    # 将target的大小缩放到与std一致
    target = cv2.resize(target, std.shape[::-1])
    res = cv2.matchTemplate(target, std, cv2.TM_CCOEFF_NORMED)
    # 返回值分别是min_val,max_val,min_loc,max_loc
    return cv2.minMaxLoc(res)[1]  # 只要maxval


def getNumber(src):
    '''将一张图片与全体模板比较，取最大相似的字符作结果'''
    maxv, maxchar = 0, '?'
    for fi in range(2):
        for i in strname:
            v = compare(src, tems[fi][i])
            if v > maxv:
                maxv, maxchar = v, i
            # print('(%s %s %.2f)' % (fi, i, v), end=' ')
        # print()
    # print()
    return maxchar


def match(srcs):
    '''将分割图像列表与模板比较,返回结果'''
    return [getNumber(i) for i in srcs]


def getMatch(img):
    '''给定二值化图像，输出识别结果数组'''
    srcs = splitNumbers(img)
    return [getNumber(i) for i in srcs]


# 效果展示
'''
from stringSplit import *
from saveImg import saveImgs
img = cv2.imread('../../imgs/10.png')
img = toGrey(img)
img = toBinary(img, getThrestHold(img))
sumHori, sumVert = getHoriAndVertSum(img)
l, r = getNumberLineRange(sumHori)
img2 = img[l:r, :]
sumHori2, sumVert2 = getHoriAndVertSum(img2)
rng = filtRanges(getRanges(sumVert2))
imgs = splitByVerts(img2, rng)
# saveImgs(imgs)
res = match(imgs)
[print(i, end='') for i in res]
'''
