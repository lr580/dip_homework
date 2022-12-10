# import cv2
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


# 初版代码
"""
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
"""


def getRanges(sums, low=0.32):
    '''输入向量,返回所有值>=low*均值的连续峰段'''
    lim = low*sums.mean()
    ans = []  # 所有函数值>=lim的区间端点[l,r]
    inLow = True  # 当前是否扫描到<lim的下标
    left, right = -1, -1  # 临时变量
    n = sums.shape[0]  # 总长
    for i in range(n):
        # 进入符合条件的区间
        if sums[i] >= lim and inLow:
            left, inLow = i, False
        # 退出符合条件的区间
        if sums[i] < lim and not inLow:
            right, inLow = i, True
            ans.append([left, right])
    return ans


def getNumberLineRange(sums, low=0.35):
    '''输入向量,返回一个数字行的下标范围[l,r]'''
    low = sums.mean()*low
    rng = getRanges(sums)
    if len(rng) == 0:  # 图片有误
        return [0, 0]
    # 找到最长的段对应的下标
    strip = max(rng, key=lambda x: x[1]-x[0])
    sid = rng.index(strip)
    if sid > 0:  # 上一段
        return rng[sid-1]
    if sid+1 < len(rng):  # 下一段
        return rng[sid+1]
    return [0, 0]  # 只有条形码


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


# 初版算法
"""
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
"""


def filtRanges(img, arr):
    '''输入区间列表,返回经过初步筛选后的有效区间列表'''
    res = []
    h = img.shape[0]
    for l, r in arr:
        sub = img[:, l:r+1]
        blacks = sub[sub == 0].size
        lens = r-l+1
        tot = h*lens
        if blacks >= tot*0.7:  # 黑色太多
            continue
        sumH, sumV = getHoriAndVertSum(sub)
        vrows = sumH[sumH > 0.05*h].size
        if vrows < 0.28*h:  # 空白行太多
            continue
        res.append([l, r])
    return res


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
    rng = filtRanges(img2, getRanges(sumVert2, 0.12))
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


# 调试用
def plotSplit(img0):
    '''绘图(输出数字行和分割字符)'''
    img = toGrey(img0)
    img = toBinary(img, getThrestHold(img))
    sumHori, sumVert = getHoriAndVertSum(img)
    l, r = getNumberLineRange(sumHori)
    img2 = img[l:r, :]
    sumHori2, sumVert2 = getHoriAndVertSum(img2)
    # 可以注释掉下面代码，查看取消筛选的效果
    # 换用这行代码：
    # rng = getRanges(sumVert2)
    rng = filtRanges(img2, getRanges(sumVert2))
    imgs = splitByVerts(img2, rng)
    saveImgs(imgs)
    plt.subplot(211)
    plt.imshow(img, 'gray')
    plt.subplot(212)
    plt.imshow(img2, 'gray')
    plt.show()


# 调试用
def plotNumberLineAnalyse(img0):
    '''绘图只输出数字行及其统计特征'''
    img = getBinary(img0)
    sumHori, sumVert = getHoriAndVertSum(img)
    l, r = getNumberLineRange(sumHori)
    img2 = img[l:r, :]
    sumHori2, sumVert2 = getHoriAndVertSum(img2)
    plt.subplot(211)
    plt.imshow(img2, 'gray')
    plt.subplot(212)
    plt.plot(sumVert2)
    plt.show()


# 效果展示
'''
img = cv2.imread('../../imgs/02.png')
plotSumAnalyse(img)
plotSplit(img)
plotNumberLineAnalyse(img)
'''
