#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import division             # Division in Python 2.7
import matplotlib
matplotlib.use('Agg')                       # So that we can render files without GUI
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import math

from matplotlib import colors

#wczytywanie wys., szer., odgegł., i macierzy wysokości
def loadValues(name):
    with open(name, 'r') as plik: 
        matrix = plik.read().splitlines()
    matrix = [ line.split(' ') for line in matrix ]
    height = float(matrix[0][0])
    width = float(matrix[0][1])
    dist = float(matrix[0][2])
    del matrix[0]
    for i in range(len(matrix)):
        del matrix[i][-1]
        for j in range(len(matrix[i])):
            matrix[i][j] = float(matrix[i][j])
    return(matrix, height, width, dist)

def scaling_matrix(matrix, start_pt, end_pt, shadow_scale):
    minimum = min([ min(element) for element in matrix])
    maximum = max([ max(element) for element in matrix])
    i = len(matrix)
    j = len(matrix[0])
    for row in range(i):
        for column in range(j):
            matrix[row][column] = (matrix[row][column] - minimum) / (maximum - minimum)
            h, s, v = transition3(matrix[row][column], start_pt, end_pt)
            if column != 0:
                if (old < (matrix[row][column])):
                    v = v + shadow_scale
                    if v > 1:
                        v = 1
            old = matrix[row][column]            
            matrix[row][column] = hsv2rgb(h, s, v)
    return(matrix)

def hsv2rgb(hue, sat, val):
    hue60 = hue / 60.0
    hue60f = math.floor(hue60)
    hueint = int(hue60f) % 6
    frac = hue60 - hue60f
    p = val * (1 - sat)
    q = val * (1 - frac * sat)
    t = val * (1 - (1 - frac) * sat)
    r, g, b = 0, 0, 0
    if hueint == 0:
        r, g, b = val, t, p
    elif hueint == 1:
        r, g, b = q, val, p
    elif hueint == 2:
        r, g, b = p, val, t
    elif hueint == 3:
        r, g, b = p, q, val
    elif hueint == 4:
        r, g, b = t, p, val
    elif hueint == 5:
        r, g, b = val, p, q
    return (r, g, b)  
    
def transition(value, start_point, end_point):
    return start_point + (end_point - start_point)*value

def transition3(value, s, e):
    r = transition(value, s[0], e[0])
    g = transition(value, s[1], e[1])
    b = transition(value, s[2], e[2])
    return (r, g, b)      
    
def plot_map(matrix, height, width, name):
    rc('legend', fontsize=10)
    fig = plt.figure()
    plt.imshow(matrix, shape = (height, width, 3), aspect = 'auto')
    fig.savefig(name)
    return(0, 0, 0, 0)
        
if __name__ == '__main__':
    matrix, height, width, dist = loadValues("big.dem")
    matrix = scaling_matrix(matrix, [120, 1, 1], [0, 1, 1], 0.3)
    plot_map(matrix, height, width, "my_map.pdf")
    
    
    
