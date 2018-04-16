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
    print("Drawing blc_wht...")
    num = len(imageList)
    cols = min(num, 3)
    rows = num // cols
    if(num % cols != 0):
        rows += 1
    fig, plots = plt.subplots(rows, cols, figsize=(cols * 6, rows * 4))
    for r in range(rows):
        for c in range(cols):
            if(r * cols + c < num):
                plots[r,c].imshow(imageList[r * cols + c], cmap = 'gray')
                plots[r,c].tick_params(axis='both', which='both', bottom='off', top='off', left='off', right='off', labelleft='off', labelbottom='off')
    
    plt.tight_layout()
    fig.savefig('blc_wht5.pdf', facecolor='black')
    plt.close()
    print("Drawing col_edges...")
    fig, plots = plt.subplots(rows, cols, figsize=(cols * 3, rows * 2))
    for r in range(rows):
        for c in range(cols):
            if(r * cols + c < num):
                plots[r,c].imshow(firstList[r * cols + c])
                plots[r,c].tick_params(axis='both', which='both', bottom='off', top='off', left='off', right='off', labelleft='off', labelbottom='off')
    
    plt.tight_layout()
    fig.savefig('col_edges5.pdf')
    plt.close()

def changeColor(i):
    i += 1
    if(i == 3):
        i = 0
    return i    

def setImages(lista):
    resultList = []
    resultList2 = []
    colorList = [(255,0,0), (0,255,0), (0,0,255)]
    colorCheck = 0
    for pic in lista:
        print(pic)
        image = cv2.imread(pic)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR);
        #uzyskanie lepszego kontrastu miedzy samolotem a niebem
        imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((5,5), np.uint8)
        imgray = cv2.morphologyEx(imgray, cv2.MORPH_OPEN, kernel)
        
        imgray = cv2.GaussianBlur(imgray, (3,3), 0)
        imgray = cv2.erode(imgray, kernel, iterations = 2)
        imgray = cv2.dilate(imgray, kernel, iterations = 2)
        #imgray = cv2.morphologyEx(imgray, cv2.MORPH_CLOSE, kernel)
        #kontury do kolorowania
        ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        #ret, thresh = cv2.threshold(imgray, 129, 255, 0)
        image2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #image2[::] = 0
        #obliczenie sredniej w powierzchni wewnatrz konturow
        sum = 0
        for con in contours:
            sum += cv2.contourArea(con)
        mean = (sum / max(len(contours), 1) / 30)
        #nakladnie konturow
        for con in contours:
            if(cv2.contourArea(con) > mean):
                colorCheck = changeColor(colorCheck)
                image = cv2.drawContours(image, con, -1, colorList[colorCheck], 3)
                #image2 = cv2.drawContours(image2, con, -1, (255,255,255), 3)
        image2 = filters.sobel(image2)
        
        image2 = cv2.dilate(image2, kernel, iterations = 1)
        image2 = cv2.erode(image2, kernel, iterations = 1)
        
        resultList.append(image2) 
        resultList2.append(image)       
    return resultList, resultList2
              
if __name__ == '__main__':
    #planes = ["-01.jpg", "-07.jpg", "-08.jpg",  "-10.jpg", "-11.jpg", "-17.jpg","-09.jpg", "-12.jpg", "-16.jpg", "-02.jpg", "-05.jpg", "-06.jpg"]
    planes = ["-01.jpg", "-02.jpg", "-03.jpg",  "-04.jpg", "-05.jpg", "-06.jpg","-07.jpg", "-08.jpg", "-09.jpg", "-10.jpg", "-11.jpg", "-12.jpg","-13.jpg", "-14.jpg", "-15.jpg", "-16.jpg", "-17.jpg","-18.jpg", "-19.jpg", "-20.jpg"]
    planesList = ([toname(p) for p in planes])
    
    contourList, clearList = setImages(planesList)
    drawPicture(contourList, clearList)
