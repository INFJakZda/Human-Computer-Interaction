from skimage import filters,data,color,measure,exposure
import numpy as np
import argparse
import cv2
from matplotlib import pyplot as plt
from pylab import *
from PIL import Image

if __name__ == '__main__':
    def toname(g):
        return g.replace('-', '/home/jakub/Pulpit/KCK/3_obrazy/samoloty/images/samolot')
    
    planes = ["-01.jpg", "-07.jpg", "-08.jpg", "-09.jpg", "-10.jpg", "-05.jpg"]
    
    planes_list = ([toname(p) for p in planes])
     
    for pic in planes_list:
        image = array(Image.open(pic).convert('L'))
        ret,thresh = cv2.threshold(image,245,255,0)
        im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

        tam = 0
        contornoGrande = 0
        for contorno in contours:
            if len(contorno) > tam:
                contornoGrande = contorno
                tam = len(contorno)

        cv2.drawContours(image,contornoGrande,-1,(0,255,0),2)

        cv2.imshow('My image',image)
        
        show()
