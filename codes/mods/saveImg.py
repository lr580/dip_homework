import os
import matplotlib.image as mpimg


def saveImgs(imgs, path='output'):
    '''保存图片列表的全部图片到指定路径文件夹内'''
    if not os.path.exists(path):
        os.mkdir(path)
    for i in range(len(imgs)):
        dest = os.path.join(path, str(i)+'.png')
        mpimg.imsave(dest, imgs[i], cmap='gray')
