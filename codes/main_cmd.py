from mods.toGrey import toGrey
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
img = mpimg.imread('a.jpg')
img2 = toGrey(img)
print(img.shape, img2.shape)
plt.imshow(img2)
plt.show()
toGrey()
