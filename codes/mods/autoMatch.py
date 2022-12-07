from preRotate import *
from graphCut import *
from stringMatch import *


#调试
def prints(res):
    [print(i, end='') for i in res]
    print()


def betterMatch(m1,m2):
    '''给定两个匹配结果，选择最优的'''


def autoMatch(img):
    '''给定一张图片，输出其ISBN字符串结果\n'''
    img = autoRotateC(img)
    thr = getThrestHold(toGrey(img))
    img1 = autoCut(img, thr)
    img2 = rotateImg(img1, 180)
    res1 = getMatch(img1)
    res2 = getMatch(img2)
    prints(res1)
    prints(res2)


import cv2
img = cv2.imread('../../imgs/09.png')
autoMatch(img)