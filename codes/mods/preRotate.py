import cv2
from toGrey import toGrey
from toBinary import toBinary, getThrestHold
from stringSplit import *
from math import tan

# 倍增法+边缘检测+Hough直线检测 效果展示
'''
img = cv2.imread('../../imgs/07.png')
img = toGrey(img)
img = toBinary(img, getThrestHold(img))
# plotSumAnalyse(img, False)
# 50,150是最小最大阈值,3是sobel卷积核大小
edges = cv2.Canny(img, 50, 150, apertureSize=3)
# lim 是直线上的最小点数
lim = int(np.min(img.shape)*0.8)
while True:
    lines = cv2.HoughLines(edges, 1, np.pi/180, lim)
    # if lim <= np.min(img.shape)*0.2:#实在找不到就算了
    #     break
    if type(lines) == type(None) or len(lines) <= 5:
        lim = int(lim*0.9)  # 找不到/太少就不断缩小要求
        continue
    break
img2 = img.copy()
if type(lines) != type(None):
    print(len(lines))
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        # 输入参数： img， 起始点， 终， 颜色， 宽度
        cv2.line(img2, (x1, y1), (x2, y2), (0, 0, 255), 2)
        k = np.arctan2(y2-y1, x2-x1)
        print(line[0][1]/np.pi*180)
        # print(k,k/np.pi*180)
else:
    print('not found')
plt.subplot(131)
plt.imshow(img, 'gray')
plt.subplot(132)
plt.imshow(edges, 'gray')
plt.subplot(133)
plt.imshow(img2, 'gray')
plt.show()
'''


def getLines(img):
    '''传入二值化图像,输出其倍增法所有检测出来的直线'''
    edges = cv2.Canny(img, 50, 150, apertureSize=3)
    # lim 是直线上的最小点数
    lim = int(np.min(img.shape)*0.8)
    while True:
        lines = cv2.HoughLines(edges, 1, np.pi/180, lim)
        if type(lines) == type(None) or len(lines) <= 5:
            lim = int(lim*0.9)  # 找不到/太少就不断缩小
            continue
        return lines


def getMidAngle(lines):
    '''给定极坐标直线组,返回位于中位数斜角(角度制)'''
    lt = []
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        k = np.arctan2(x2-x1, y2-y1)
        lt.append(k/np.pi*180)
    lt.sort()
    return lt[lines.shape[0]//2]
    # 方案二：(缺点:角度不明确)
    # l = np.sort(lines[:, 0, 1])
    # return l[l.size//2]


def rotateImg(img, ang):
    '''以中心旋转图像,顺时针转动ang角度并返回(白色填充)'''
    h, w = img.shape[:2]
    cx, cy = w//2, h//2
    # 1.0表示不缩放
    m = cv2.getRotationMatrix2D((cx, cy), -ang, 1.0)
    mc, ms = np.abs(m[0, 0:2])
    nw = int(h*ms+w*mc)
    nh = int(h*mc+w*ms)
    m[0, 2] += (nw/2)-cx
    m[1, 2] += (nh/2)-cy
    numBlack = img[img == 0].size
    numWhite = img.size-numBlack
    if numBlack > numWhite:
        c = (0, 0, 0)
    else:
        c = (255, 255, 255)
    return cv2.warpAffine(img, m, (nw, nh),
                          borderValue=c)


def autoRotate(img):
    '''以二值化图像为输入，输出自动旋转后的图像'''
    lines = getLines(img)
    ang = getMidAngle(lines)
    return rotateImg(img, ang)


def autoRotateC(img):
    '''以彩色图像为输入，输出自动旋转后的图像'''
    img2 = toGrey(img)
    img2 = toBinary(img2, getThrestHold(img2))
    lines = getLines(img2)
    ang = getMidAngle(lines)
    return rotateImg(img, ang)


# 自动旋转 展示
'''
img = cv2.imread('../../imgs/07.png')
img = toGrey(img)
img = toBinary(img, getThrestHold(img))
lines = getLines(img)
ang = getMidAngle(lines)
img2 = rotateImg(img, ang)
plt.subplot(121)
plt.imshow(img, 'gray')
plt.subplot(122)
plt.imshow(img2, 'gray')
plt.show()
'''
