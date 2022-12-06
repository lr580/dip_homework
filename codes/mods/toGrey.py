import numpy as np


#等效:cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
def toGrey(img):
    '''函数功能:传入img,将其灰度化并返回\n
    根据课件内容, 采用加权平均的方法做灰度化效果更好\n
    为了加速运算, 使用矩阵运算而不是 for-for 迭代\n
    为了方便后续处理,维度将保持不变\n
    建议输入:[0,255]整数表示灰度,只有RGB无alpha通道\n'''
    if len(img.shape) == 2:  # 已经是灰度图像了
        return img
    rd = img.shape[2]  # 可能是3/4(png有alpha通道)
    line = [0.299, 0.587, 0.114, 0][:rd]
    trans = np.array(line).transpose()  # 矩阵转置
    img2 = np.dot(img, trans).astype(img.dtype)
    img2 = np.reshape(img2, img.shape[:2])
    return img2


# 下面是 toGrey 的测试用例
'''
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
img = mpimg.imread('../a.jpg') #任意彩色图片
img2 = toGrey(img)
print(img.shape, img2.shape)
plt.imshow(img2,'gray')
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
plt.imshow(img2,'gray')#not greys
plt.show()
'''
