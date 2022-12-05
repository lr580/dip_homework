import numpy as np


def toGrey(img):
    '''函数功能:传入img,将其灰度化并返回\n
    根据课件内容, 采用加权平均的方法做灰度化效果更好\n
    为了加速运算, 使用矩阵运算而不是 for-for 迭代\n
    为了方便后续处理,维度将保持不变'''
    rd = img.shape[2]  # 可能是3/4(png有alpha通道)
    line = [0.299, 0.587, 0.114, 0][:rd]
    arr = [line for i in range(rd)]
    trans = np.array(arr).transpose()  # 矩阵转置
    img2 = np.dot(img, trans).astype(img.dtype)
    return img2


# 下面是 toGrey 的测试用例
'''
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
img = mpimg.imread('../a.jpg') #任意彩色图片
img2 = toGrey(img)
print(img.shape, img2.shape)
plt.imshow(img2)
plt.show()
toGrey()
'''

# 下面是 toGrey 的效果展示代码
'''
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
img = mpimg.imread('../a.png')
img2 = toGrey(img)
# print(img[0,0],img2[0,0])
plt.subplot(121)
plt.imshow(img)
plt.subplot(122)
plt.imshow(img2)
plt.show()
'''
