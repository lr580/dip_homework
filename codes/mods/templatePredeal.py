import cv2
import os
import matplotlib.image as mpimg
from toGrey import toGrey
from toBinary import toBinary, getThrestHold
from stringSplit import *
# from saveImg import saveImgs

strname = [i for i in '0123456789_-X']


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
#旧版
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
