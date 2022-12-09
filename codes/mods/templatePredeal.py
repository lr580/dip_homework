import cv2
import os
import matplotlib.image as mpimg
from toGrey import toGrey
from toBinary import toBinary, getThrestHold
from stringSplit import *
# from saveImg import saveImgs

# strname = [i for i in '0123456789_-XISBN']
strname = [i for i in '0123456789XISBN-']


def preDealTemplate(fontIndex):
    '''给定字体编号，对该字体进行分割并保存'''
    # 读图并灰度化、二值化,路径可能要自己改
    path = '../template'
    srcPath = os.path.join(path, 'raw%d.png' % fontIndex)
    src = cv2.imread(srcPath)
    src = toGrey(src)
    src = toBinary(src, getThrestHold(src))
    sumH, sumV = getHoriAndVertSum(src)
    rng = getRanges(sumV)
    imgs = splitByVerts(src, rng)
    # saveImgs(imgs, path, str(fontIndex)+'_')
    for i in range(len(strname)):
        name = '%d_%s.png' % (fontIndex, strname[i])
        dest = os.path.join(path, name)
        mpimg.imsave(dest, imgs[i], cmap='gray')


# 旧版
"""
def preDealTemplate(fontIndex):
    '''给定字体编号，对该字体进行分割并保存'''
    # 读图并灰度化、二值化,路径可能要自己改
    path = '../template'
    srcPath = os.path.join(path, 'raw%d.png' % fontIndex)
    src = cv2.imread(srcPath)
    src = toGrey(src)
    src = toBinary(src, getThrestHold(src))
    sumH, sumV = getHoriAndVertSum(src)
    rng = getRanges(sumV)
    imgs = splitByVerts(src, rng)
    # saveImgs(imgs, path, str(fontIndex)+'_')
    for i in range(len(strname)):
        name = '%d_%s.png' % (fontIndex, strname[i])
        dest = os.path.join(path, name)
        mpimg.imsave(dest, imgs[i], cmap='gray')
for i in range(1, 4):
    preDealTemplate(i)
"""

# for i in range(4, 5):
#     preDealTemplate(i)

# 预处理用(已废弃)


def readFromImgs(src):
    '''读取已有的文件夹jpg图片并将其反色存png'''
    srcp = os.path.join('../t0', src+'.jpg')
    desp = os.path.join('../template', '4_%s.png' % src)
    img = cv2.imread(srcp)
    img = getBinary(img)
    img = 255-img
    mpimg.imsave(desp, img, cmap='gray')


# for i in 'ISBN':
#     readFromImgs(i)


def preDealFonts():
    '''读取已有的文件夹jpg图片并将其反色存png'''
    for i in range(1, 3):
        for j in strname:
            srcp = os.path.join('../t0', '%s.%d.jpg' % (j, i))
            desp = os.path.join('../template', '%d_%s.png' % (4+i, j))
            img = cv2.imread(srcp)
            img = getBinary(img)
            img = 255-img
            mpimg.imsave(desp, img, cmap='gray')

# preDealFonts()