import cv2
from toGrey import toGrey
from toBinary import toBinary, getThrestHold
from preRotate import autoRotate
from stringSplit import plotSumAnalyse

img = cv2.imread('../../imgs/08.png')
img = toGrey(img)
img = toBinary(img, getThrestHold(img))
# img2 = autoRotate(img)
plotSumAnalyse(img, False)
