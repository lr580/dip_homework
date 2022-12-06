import numpy as np
import cv2
from toGrey import toGrey


def getThrestHold(img):
    '''传入灰度化的图像(要求维度n*m),灰度取整[0,255]\n
    使用Otsu算法求出阈值并返回该阈值x∈[0,255]'''
    n, m = img.shape
    mx, x = -1, 0  # mx是当前最大值,x是取得最值的阈值
    np.seterr(divide='ignore', invalid='ignore')  # 零除
    for i in range(0, 256):
        n0 = np.sum(img < i)
        n1 = n*m-n0
        w0 = n0/(n*m)
        w1 = 1-w0
        mu0 = np.sum(img[img < i])/n0
        mu1 = np.sum(img[img >= i])/n1
        g = w0*w1*(mu0-mu1)**2
        if g > mx:
            mx, x = g, i
    return x


def toBinary(img, x, ltx=0, gex=255):
    '''函数功能:传入彩图img和阈值x,将其二值化并返回\n
    规定<x的染成白色(ltx),>=x的染成灰色(gex)'''
    img2 = img.copy()
    img2[img2 < x] = ltx
    img2[img2 >= x] = gex
    return img2


# 算法测试与展示
'''
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
img = cv2.imread('../b.png')
img0 = toGrey(img)
img2 = toBinary(img0, getThrestHold(img0))
plt.subplot(121)
plt.imshow(img)
plt.subplot(122)
plt.imshow(img2,'gray')
plt.show()
'''

# 算法比较：库函数调用
'''
def toBinary(img):
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = toGrey(img)
    th, img2 = cv2.threshold(img, 0, 256, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    print(th)
    return img2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
# img =mpimg.imread('../a.png') #(实数[0,1]且有alpha)
img =cv2.imread('../a.png') #(整数[0,255]且无alpha)
print(img[0,0])
print(img.shape)
img2 = toBinary(img)
plt.subplot(121)
plt.imshow(img)
plt.subplot(122)
plt.imshow(img2,'gray')
plt.show()
'''
