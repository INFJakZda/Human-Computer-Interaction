import numpy as np
import cv2
from matplotlib import pyplot as plt
from skimage import filters,data,color,measure,exposure,feature
import argparse
from pylab import *
from PIL import Image

def toname(g):
        return g.replace('-', './images/samolot')

def drawPicture(imageList, firstList):
    num = len(imageList)
    cols = min(num, 3)
    rows = num // cols
    if(num % cols != 0):
        rows += 1
    print(type(imageList[0]))
    fig, plots = plt.subplots(rows, cols, figsize=(cols * 6, rows * 4))
    for r in range(rows):
        for c in range(cols):
            if(r * cols + c < num):
                plots[r,c].imshow(imageList[r * cols + c], cmap = 'gray')
                plots[r,c].tick_params(axis='both', which='both', bottom='off', top='off', left='off', right='off', labelleft='off', labelbottom='off')
    
    plt.tight_layout()
    fig.savefig('ex1.pdf', facecolor='black')
    plt.close()
    
    fig, plots = plt.subplots(rows, cols, figsize=(cols * 3, rows * 2))
    for r in range(rows):
        for c in range(cols):
            if(r * cols + c < num):
                plots[r,c].imshow(firstList[r * cols + c])
                plots[r,c].tick_params(axis='both', which='both', bottom='off', top='off', left='off', right='off', labelleft='off', labelbottom='off')
    
    plt.tight_layout()
    fig.savefig('ex2.pdf')
    plt.close()

def changeColor(i):
    i += 1
    if(i == 6):
        i = 0
    return i    

def setImages(lista):
    resultList = []
    resultList2 = []
    colorList = [(255,0,0), (255,0,0), (0,255,0), (0,255,0), (0,255,0), (255,0,0)]
    colorCheck = 0
    for pic in lista:
        image = cv2.imread(pic)
        
        ret,thresh = cv2.threshold(image,127,255,0)
        im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

        tam = 4
        contornoGrande = 0
        for contorno in contours:
            if len(contorno) > tam:
                contornoGrande = contorno
                tam = len(contorno)

        cv2.drawContours(image,contornoGrande,-1,(0,255,0),2)
        
        #uzyskanie lepszego kontrastu miedzy samolotem a niebem
        imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        #kontury do kolorowania
        ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        image2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #print(contours)
        i = 0        
        for con in contours:
            for ones in con:
                print(len(ones))
                colorCheck = changeColor(colorCheck)
                image = cv2.drawContours(image, con, -1, colorList[colorCheck], 3)
                image2 = cv2.drawContours(image2, con, -1, (0,255,0), 3)
                i += 1  
        image2 = filters.sobel(image2)
        print(i)
        
        resultList.append(image2) 
        resultList2.append(image)       
    return resultList, resultList2
              
if __name__ == '__main__':
    planes = ["-01.jpg", "-07.jpg", "-08.jpg",  "-10.jpg", "-11.jpg", "-17.jpg"]
    
    planesList = ([toname(p) for p in planes])
    
    planesList, clearList = setImages(planesList)
    drawPicture(planesList, clearList)
