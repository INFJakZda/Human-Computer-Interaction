from skimage import filters,data,color,measure,exposure
import numpy as np
import argparse
import cv2
from matplotlib import pyplot as plt

if __name__ == '__main__':
    def toname(g):
        return g.replace('-', '/home/jakub/Pulpit/KCK/3_obrazy/samoloty/images/samolot')
    
    planes = ["-01.jpg", "-07.jpg", "-08.jpg", "-09.jpg", "-10.jpg", "-05.jpg"]
    
    planes_list = ([toname(p) for p in planes])
     
    for pic in planes_list: '''
        #image = data.load(pic, as_grey = True)
        #image = filters.sobel(image)
        #plt.imshow(image, cmap = plt.cm.gray)
        #plt.show()
        
        #img = img_as_float(data.imread(pic))
        #io.imshow(skimage.feature.canny(img, sigma=3))
        image = cv2.imread(pic)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        edged = cv2.Canny(gray, 50, 200)
        edged = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
        #cv2.imshow("plane", edged)
        plt.imshow(edged, cmap = plt.cm.gray)
        plt.show() '''
        
        ret,thresh = cv2.threshold(image,245,255,0)
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

        tam = 0

        for contorno in contours:
            if len(contorno) > tam:
                contornoGrande = contorno
                tam = len(contorno)

        cv2.drawContours(image,contornoGrande.astype('int'),-1,(0,255,0),2)

        cv2.imshow('My image',image)
        
        
    '''    
    
    image = data.load("/home/jakub/Pulpit/KCK/3_obrazy/samoloty/images/samolot08.jpg", as_grey = True)
    plt.imshow(image)
    plt.show()
    image = filters.sobel(image)
    plt.imshow(image, cmap = plt.cm.gray)
    plt.show() '''
