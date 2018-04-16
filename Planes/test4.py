import numpy as np
import cv2
from matplotlib import pyplot as plt

im = cv2.imread('./images/samolot07.jpg')

imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(imgray, 127, 255, 0)

im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

im2 = cv2.drawContours(im2, contours, -1, (0,255,0), 3)

im2 = im2

im2 = cv2.Canny(im2)

cv2.imshow(im2)


#plt.imshow(im2, cmap = 'gray')
#plt.show()
