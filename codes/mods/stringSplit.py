from saveImg import saveImgs
import numpy as np
import matplotlib.pyplot as plt
from toBinary import *

# 统计图
'''
img = cv2.imread('../../imgs/02.png')
img = toGrey(img)
img = toBinary(img, getThrestHold(img))
img1 = ((255-img)//255).astype(np.uint16)
sumVert = img1.sum(axis=0)
sumHori = img1.sum(axis=1)
plt.subplot(221)
plt.imshow(img, 'gray')
# lt = list(range(img.shape[0]-1, -1, -1))
plt.subplot(223)
plt.plot(sumVert)
plt.subplot(224)
plt.plot(sumHori)
plt.subplot(222)
lt = list(range(img.shape[0]))
plt.ylim(img.shape[0], 0)  # 这个倒了lt自己也会倒
plt.plot(sumHori, lt)
plt.show()
'''


def getHoriAndVertSum(img):
    '''输入二值化图像,依次返回其行列黑色点和向量'''
    img1 = ((255-img)//255).astype(np.uint16)
    sumVert = img1.sum(axis=0)
    sumHori = img1.sum(axis=1)
    return [sumHori, sumVert]


def getNumberLineRange(sums, low=0.25):
    '''输入向量,返回逆序寻找的第一个数字行'''
    lim = np.max(sums)*low  # 实际阈值
    left, right = -1, -1
    n = sums.shape[0]
    for i in range(n-1, -1, -1):
        if sums[i] >= lim and right == -1:
            right = i
        if sums[i] < lim and right != -1:
            left = i
            break
    return [max(0, left), max(0, right)]


def getRanges(sums, low=0.08):
    '''输入向量,返回顺序寻找的所有>=low的连续峰段'''
    lim = np.max(sums)*low  # 实际阈值
    ans, inLow = [], True
    left, right = -1, -1
    n = sums.shape[0]
    for i in range(n):
        if sums[i] >= lim and inLow:
            left, inLow = i, False
        if sums[i] < lim and not inLow:
            right, inLow = i, True
            ans.append([left, right])
    return ans


def splitByVerts(img, lr):
    '''输入图片和峰段,返回切割后的全部子图'''
    return [img[:, l:r+1]for l, r in lr]


# 代码示例(效果展示)
'''
img = cv2.imread('../../imgs/02.png')
img = toGrey(img)
img = toBinary(img, getThrestHold(img))
sumHori, sumVert = getHoriAndVertSum(img)

l, r = getNumberLineRange(sumHori)
img2 = img[l:r, :]
# plt.subplot(211)
# plt.imshow(img, 'gray')
# plt.subplot(212)
# plt.imshow(img2, 'gray')
# plt.show()

sumHori2, sumVert2 = getHoriAndVertSum(img2)
# plt.subplot(211)
# plt.imshow(img2, 'gray')
# plt.subplot(212)
# plt.plot(sumVert2)
# plt.show()
imgs = splitByVerts(img2, getRanges(sumVert2))
saveImgs(imgs)
'''


def filtRanges(arr, low=0.3, maxDel=6):
    '''输入区间,返回经过初步筛选后的有效区间'''
    n = len(arr)
    if n == 0:  # 无效区间
        return []
    b = [(i, arr[i][1]-arr[i][0]) for i in range(n)]
    b.sort(key=lambda v: v[1])  # 按长度排序
    lim = low*b[n//2][1]  # 中位数
    ban = {b[i][0] for i in range(min(maxDel, n))
           if b[i][1] < lim}
    arr = [arr[i] for i in range(n) if i not in ban]
    return arr


# 效果展示
'''
img = cv2.imread('../../imgs/02.png')
img = toGrey(img)
img = toBinary(img, getThrestHold(img))
sumHori, sumVert = getHoriAndVertSum(img)
l, r = getNumberLineRange(sumHori)
img2 = img[l:r, :]
sumHori2, sumVert2 = getHoriAndVertSum(img2)
rng = filtRanges(getRanges(sumVert2))
imgs = splitByVerts(img2, rng)
saveImgs(imgs)
'''


def splitNumbers(img):
    '''输入一张二值化图像，返回其分割出来的字符子图列表'''
    sumHori, sumVert = getHoriAndVertSum(img)
    l, r = getNumberLineRange(sumHori)
    img2 = img[l:r, :]
    sumHori2, sumVert2 = getHoriAndVertSum(img2)
    rng = filtRanges(getRanges(sumVert2))
    imgs = splitByVerts(img2, rng)
    return imgs


# 调试用
def plotSumAnalyse(img0, draw2Hori=True):
    '''绘制彩色图像的水平垂直频次分析'''
    img = toGrey(img0)
    img = toBinary(img, getThrestHold(img))
    sumHori, sumVert = getHoriAndVertSum(img)
    plt.subplot(221)
    plt.imshow(img, 'gray')  # 不输出原图
    plt.subplot(223)
    plt.plot(sumVert)
    if draw2Hori:
        plt.subplot(224)
        plt.plot(sumHori)
    plt.subplot(222)
    lt = list(range(img.shape[0]))
    plt.ylim(img.shape[0], 0)  # 这个倒了lt自己也会倒
    plt.plot(sumHori, lt)
    plt.show()


# import cv2
# img = cv2.imread('../../imgs/10.png')
# plotSumAnalyse(img)


# 调试用
def plotSplit(img0):
    img = toGrey(img0)
    img = toBinary(img, getThrestHold(img))
    sumHori, sumVert = getHoriAndVertSum(img)
    l, r = getNumberLineRange(sumHori)
    print(l, r)
    img2 = img[l:r, :]
    sumHori2, sumVert2 = getHoriAndVertSum(img2)
    rng = filtRanges(getRanges(sumVert2))
    imgs = splitByVerts(img2, rng)
    print(len(imgs))
    saveImgs(imgs)
    plt.subplot(121)
    plt.imshow(img, 'gray')
    plt.subplot(122)
    plt.imshow(img2, 'gray')
    plt.show()

# plotSplit(img)
