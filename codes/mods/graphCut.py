import cv2
from toGrey import toGrey
from toBinary import toBinary  # , getThrestHold
# from preRotate import autoRotate, autoRotateC
# from stringSplit import plotSumAnalyse
# import matplotlib.image as mpimg
# import matplotlib.pyplot as plt


# 现象展示
'''
img = cv2.imread('../../imgs/08.png')
img = toGrey(img)
img = toBinary(img, getThrestHold(img))
# img2 = autoRotate(img)
plotSumAnalyse(img, False)
'''


# 该函数暂时废弃
def getBetterRectImg(img):
    """给定二值化图像，返回其消除条形码内容后的矩形区域\n
    基于膨胀和腐蚀进行，但是两次使用的核不一样"""
    # 实际上是 (20x1) 的全 1 的 uint8 numpy 数组,下同
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 1))
    res = cv2.dilate(img, k)  # 膨胀,以连接
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 15))
    res = cv2.erode(res, k)  # 腐蚀,以去噪
    return res


#算法比较 - 形态学方法
'''
img0 = cv2.imread('../../imgs/03.png')
img = toGrey(img0)
img = toBinary(img, getThrestHold(img))
# img = autoRotate(img)
img2 = getBetterRectImg(img)
img3 = img0.copy()

contours, _ = cv2.findContours(
    img2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    # if w > 1.2*h and w < 1.6*h:  # 去掉太长太宽的矩形
    print('%d?%d?%d?%d' % (x, y, w, h))
    cv2.rectangle(img3, (x, y), (x+w, y+h), (0,0,100), 10)


plt.subplot(131)
plt.imshow(img0, 'gray')
plt.subplot(132)
plt.imshow(img2, 'gray')
plt.subplot(133)
plt.imshow(img3, 'gray')
plt.show()
'''

#算法2 - 直接对原图进行调整 (草稿)
'''
# img0 = cv2.imread('../../imgs/07.png')
# img = autoRotateC(img0)
img = cv2.imread('../../imgs/04.png')
imgGray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # 转灰度图
imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)  # 高斯模糊
imgCanny = cv2.Canny(imgBlur, 60, 60)  # Canny算子边缘检测

contours, hierarchy = cv2.findContours(
    imgCanny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
img2 = img.copy()
for obj in contours:
    area = cv2.contourArea(obj)  # 计算轮廓内区域的面积
    # cv2.drawContours(img2, obj, -1, (255, 0, 0), 4)  # 绘制轮廓线
    perimeter = cv2.arcLength(obj, True)  # 计算轮廓周长
    approx = cv2.approxPolyDP(obj, 0.02*perimeter, True)  # 获取轮廓角点坐标
    CornerNum = len(approx)  # 轮廓角点的数量
    x, y, w, h = cv2.boundingRect(approx)  # 获取坐标值和宽度、高度
    if CornerNum == 4:  # 矩形
        print(x, y, w, h)
        cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 0, 255), 2)

# plt.subplot(131)
# plt.imshow(img0, 'gray')
# plt.subplot(132)
# plt.imshow(img, 'gray')
# plt.subplot(133)
# plt.imshow(img2, 'gray')

plt.subplot(121)
plt.imshow(img, 'gray')
plt.subplot(122)
plt.imshow(img2, 'gray')
plt.show()
'''


def getMainRectangle(img):
    '''传入任意图像,返回其出现的最大矩形区域'''
    imgGray = toGrey(img)
    # 高斯模糊
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    # Canny算子边缘检测
    imgCanny = cv2.Canny(imgBlur, 60, 60)
    # 边缘检测,RETR_TREE可能更精准
    contours, _ = cv2.findContours(
        imgCanny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    res = []  # 答案
    nh, nw = img.shape[:2]
    totArea = nh*nw
    for obj in contours:
        # 计算轮廓内区域的面积
        area = cv2.contourArea(obj)
        if area <= 0.2*totArea:  # 矩形太小
            continue
        # 计算轮廓周长
        perimeter = cv2.arcLength(obj, True)
        # 获取轮廓角点坐标
        approx = cv2.approxPolyDP(obj, 0.02*perimeter, True)
        CornerNum = len(approx)  # 轮廓角点的数量
        # 获取坐标值和宽度、高度
        x, y, w, h = cv2.boundingRect(approx)
        if CornerNum == 4:  # 是矩形
            res.append([x, y, w, h])
    if len(res) == 0:  # 找不到
        return [0, 0, nw, nh]
    ans = max(res, key=lambda x: x[2]*x[3])  # 取出最大
    return ans


#绘图展示 - 截出来的矩形框
'''
# img0 = cv2.imread('../../imgs/09.png')
# img = autoRotateC(img0)
img = cv2.imread('../../imgs/09.png')
# img = toGrey(img)
# img = toBinary(img, getThrestHold(img))
x, y, w, h = getMainRectangle(img)
img2 = img.copy()
cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 0, 255), 3)
img3 = img[y:y+h, x:x+w]

plt.subplot(131)
plt.imshow(img, 'gray')
plt.subplot(132)
plt.imshow(img2, 'gray')
plt.subplot(133)
plt.imshow(img3, 'gray')
plt.show()
'''


def cutImage(img):
    '''传入任意图像，找到最大矩形区域子图并返回\n
    如果找不到就返回原图'''
    x, y, w, h = getMainRectangle(img)
    return img[y:y+h, x:x+w]


def autoCut(img0, thr=220):
    '''传入彩色图像，两次匹配找到最大矩形区域子图\n
    返回结果是二值化后的子图'''
    img = cutImage(img0)
    img = toGrey(img)
    img = toBinary(img, thr)
    img = cutImage(img)
    return img


# 使用示例
'''
img0 = cv2.imread('../../imgs/08.png')
img = cutImage(img0)
img2 = autoCut(img0)
plt.subplot(131)
plt.imshow(img0, 'gray')
plt.subplot(132)
plt.imshow(img, 'gray')
plt.subplot(133)
plt.imshow(img2, 'gray')
plt.show()
'''
