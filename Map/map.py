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

brightnes = 0.15            # <0.0 ; 0.5> im większe tym ciemniejszy cały obraz,    
                            # pozwala na rozjaśnienie w funkcji adv_shadow_scale,   best = 0.15
smp_shadow_scale = 0.2         # <0.0 ; 0.5> im większe tym mocniejsze cieniowanie,    best = 0.2
adv_shadow_scale = 10       # < 1  ; 50 > im większe tym mocniejsze cieniowanie,    best = 10
shadow_choise = "advance"    # "simply" - podstawowy "advance" - zaawansowany
start_color = [120, 1, 1]   # kolor najnizszych czesci terenu
end_color = [0, 1, 1]       # kolor najwyzszych czesci terenu


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

def transition(value, start_point, end_point):
    return start_point + ( (end_point - start_point) * value )

def transition3(value, st_pt, end_pt):
    val1 = transition(value, st_pt[0], end_pt[0])
    val2 = transition(value, st_pt[1], end_pt[1])
    val3 = transition(value, st_pt[2], end_pt[2])
    return (val1, val2, val3)
    
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

def set_shadow(matrix_old_pt, matrix_curr_pt, v):

    if(shadow_choise == "simply"):
        if (matrix_old_pt > matrix_curr_pt):
            v = v - smp_shadow_scale
            if v < 0: v = 0
        return (v)
        
    elif(shadow_choise == "advance"):
        v -= brightnes                          #bez tego nie mozna rozjasniac v bo przewaznie jest równy 1
        diff = matrix_curr_pt - matrix_old_pt
        v = v + diff * adv_shadow_scale
        if v < 0: v = 0
        if v > 1: v = 1
        return (v)    
    else:
        print("zła nazwa cieniowania")

def scaling_matrix(matrix, start_pt, end_pt):

    minimum = min([ min(element) for element in matrix])
    maximum = max([ max(element) for element in matrix])
    i = len(matrix)         #wiersze
    j = len(matrix[0])      #kolumny
    
    for row in range(i):    
        for column in range(j):
        
            matrix[row][column] = (matrix[row][column] - minimum) / (maximum - minimum)
            h, s, v = transition3(matrix[row][column], start_pt, end_pt)
            
            #cieniowanie##############################################################                        
            if column != 0:
                v = set_shadow(matrix_old_pt, matrix[row][column], v)
            matrix_old_pt = matrix[row][column]     #dla porównywania sąsiednich pikseli
            ##########################################################################
            
            matrix[row][column] = hsv2rgb(h, s, v)
            
    return(matrix)

def plot_map(matrix, height, width, name):
    rc('legend', fontsize=10)
    fig = plt.figure()
    plt.imshow(matrix, shape = (height, width, 3), aspect = 'auto')
    fig.savefig(name)
    return(0)
        
if __name__ == '__main__':
    matrix, height, width, dist = loadValues("big.dem")
    matrix = scaling_matrix(matrix, start_color, end_color)
    plot_map(matrix, height, width, "my_map.pdf")
        
