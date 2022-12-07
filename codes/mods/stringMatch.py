import cv2
import os
from templatePredeal import strname
from toBinary import getBinary



def loadTemplates(path='../templates'):
    '''从文件夹路径返回标准字符模板(经过二值化)'''
    t = [dict() for i in range(3)]
    for i in range(3):
        for j in strname:
            name = '%d_%s.png' % (i+1, j)
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


def getNumber(src, fontid):
    '''将一张图片与特定字体比较，取最大相似的字符作结果'''
    maxv, maxchar = 0, '?'
    for i in strname:
        v = compare(src, tems[fontid][i])
        if v > maxv:
            maxv, maxchar = v, i
    return maxchar


def compares(srcs, fontid):
    '''将分割图像列表与特定字体比较,返回结果'''
    return [getNumber(i, fontid) for i in srcs]


def match(srcs):
    '''将分割图像列表与模板比较,返回结果'''
    return [getNumber(i, 2) for i in srcs]

#调试用
def analyse(src):
    for i in strname:
        pass

# 效果展示
from stringSplit import *
from saveImg import saveImgs
img = cv2.imread('../../imgs/02.png')
img = getBinary(img)
sumHori, sumVert = getHoriAndVertSum(img)
l, r = getNumberLineRange(sumHori)
img2 = img[l:r, :]
sumHori2, sumVert2 = getHoriAndVertSum(img2)
rng = filtRanges(getRanges(sumVert2))
imgs = splitByVerts(img2, rng)
saveImgs(imgs)
print(len(imgs))
res = match(imgs)
[print(i, end='') for i in res]
