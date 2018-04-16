from skimage import filters,data,color,measure,exposure
from matplotlib import pyplot as plt
import numpy as np

#Funkcja wczytuję listę obrazów
def loadImages(fileList):
    imageList = []
    for img in fileList:
        imageList.append(data.imread(img)) #wczytywanie obrazu
    return imageList

def findEdges1(image):
    intensityP = 1
    intensityK = 20
    pp,pk = np.percentile(image,(intensityP,intensityK));
    image = exposure.rescale_intensity(image,in_range=(pp,pk))
    image = color.rgb2hsv(image)
    blackWhite = np.zeros([len(image),len(image[0])])
    for i in range(len(image)):
        for j in range(len(image[i])):
            blackWhite[i][j] =1- image[i][j][2]
            image[i][j] = [0,0,0]
    contours = measure.find_contours(blackWhite,0.3)
    return  image,contours

def drawPlotsBlack(imageList):
    fig = plt.figure(facecolor="black") # czarne tło
    i = 0
    for img in imageList:
        plt.subplot(231+i) #tworznie kolejnych subplotów
        frame = plt.gca() #Frame do usuniecia osi
        frame.axes.get_xaxis().set_visible(False) #Usuniecie osix
        frame.axes.get_yaxis().set_visible(False) #Usuniecie osiy
        image, contours = findEdges1(img) #znajdywanie krawedzi
        for n,contours in enumerate(contours):
            plt.plot(contours[:,1],contours[:,0],linewidth=0.8,color="w") #Rysowanie konturu na obrazie
        plt.imshow(image)
        i +=1 #kolejny obraz
    plt.tight_layout() #Aby obrazy znajdowały się obok siebie
    plt.show()
    fig.savefig("out/samoloty.pdf",facecolor="black")
    plt.close()

if __name__ == '__main__':
    fileList = ["./images/samolot01.jpg","./images/samolot07.jpg","./images/samolot08.jpg","./images/samolot09.jpg","./images/samolot10.jpg","./images/samolot12.jpg"];
    imageList = loadImages(fileList)
    drawPlotsBlack(imageList)
