#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv
import matplotlib.pyplot as plt
import numpy

filesToRead = ['rsel.csv', 'cel-rs.csv', '2cel-rs.csv', 'cel.csv', '2cel.csv']
namesToChars = ['1-Evol-Rs', '1-Coev-RS', '2-Coev-RS', '1-Coev', '2-Coev']

def main():
    avgF = lambda List: float(sum(List)) / max(len(List), 1)
    dataDiction = {}
    markerSet = ['o', 'v', 'D', 's', 'd']
    lineColor = ['#0385F7', '#179B03', '#B70303', 'black', '#BF00CD']
    
    # Load data from csv files
    for file in filesToRead:
        with open("data/" + file, 'r') as f:
            readCsv = csv.reader(f)
            i = 0
            dataListHelperTwo = []
            for row in readCsv:
                # This two if block is to remove first trash info
                if i == 0:
                    i += 1
                elif i == 1:
                    dataListHelperOne = []
                    dataListHelperOne.append(row[0])
                    dataListHelperOne.append(row[1])
                    tempList = []
                    
                    for x in range(2, 34):
                        tempList.append(float(row[x]))
                    
                    dataListHelperOne.append(avgF(tempList))
                    dataListHelperTwo.append(dataListHelperOne)
                    
            dataDiction[file] = dataListHelperTwo
    # ********************************************************************************
    # CHAR PLOT
    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    ax2 = ax1.twiny()
        
    for ftr in range(0, 5):
        x = []
        y = []
        marker_style = dict(marker = markerSet[ftr], markersize = 4, markeredgecolor = 'black', 
                            markerfacecoloralt = lineColor[ftr], markevery = 25)
        for i in range(0, 200):
            x.append(int(dataDiction[filesToRead[ftr]][i][1])/1000)
            y.append(dataDiction[filesToRead[ftr]][i][2]*100)

        ax1.plot(x,y, color = lineColor[ftr], linewidth = 0.6, label = namesToChars[ftr], 
                 linestyle = '-', **marker_style)
    
    ax1.grid(b=True, which='major', color='tab:gray', linestyle=':')
    
    ax1.set_ylabel('Odsetek wygranych gier [%]')
    ax1.set_xlabel('Rozegranych gier (x1000)')
    ax1.set_xlim(0,500)    
    ax1.set_ylim(60,100)
    ax1_ticks = ax1.get_xticks()
    ax2.set_xlim(0,200)
    ax2_scale = ax1_ticks / 2.5    
    ax2.set_xticks(ax2_scale)
    ax2.set_xlabel('Pokolenie') 
    
    legend = ax1.legend(loc='lower right', shadow=True)
    frame = legend.get_frame()
    frame.set_facecolor('0.90')

    for label in legend.get_texts():
        label.set_fontsize('small')

    for label in legend.get_lines():
        label.set_linewidth(1.5)
        
    #  *****************************************************************************
    # CHAR BOXPOLT
    dataDiction = []
    for file in filesToRead:
        listHelp = []
        with open("data/" + file, 'r') as f:
            lastrow = None
            for lastrow in csv.reader(f):
                pass
            for x in range(2, 34):
                listHelp.append(float(lastrow[x]) * 100)
            dataDiction.append(listHelp)      
    ax1 = fig.add_subplot(122)
    ax1.yaxis.tick_right()
    for tick in ax1.get_xticklabels():
        tick.set_rotation(25)
    ax1.set_ylim(60,100)
    flierprops = dict(marker = '+', markerfacecolor = 'b', markersize = 4,
                  linestyle = 'none', markeredgecolor = 'b')
    meanpointprops = dict(marker = 'o', markeredgecolor = 'black', 
                          markerfacecolor = 'blue', markersize = 4)
    bp = ax1.boxplot(dataDiction, 1, labels = namesToChars, flierprops = flierprops, 
                     showmeans = True, meanline = False, meanprops = meanpointprops)
    ax1.grid(b=True, which='major', color='tab:gray', linestyle=':')
    plt.setp(bp['boxes'], color='blue')
    for whisker in bp['whiskers']:
        whisker.set(color='#2B00FF',lw=1)
        whisker.set_linestyle('--')
    
    plt.savefig('out/test.pdf')
    plt.close()

if __name__ == '__main__':
    main()
