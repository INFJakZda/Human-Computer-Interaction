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

rgbBw = [[0,0,0],[1,1,1]]
rgbGbr = [[0,1,0],[0,0,1],[1,0,0]]
rgbGbrFull = [[0,1,0],[0,1,1],[0,0,1],[1,0,1],[1,0,0]]
rgbWbCustom = [[1,1,1],[1,0,1],[0,0,1],[0,1,1],[0,1,0],[1,1,0],[1,0,0],[0,0,0]]

hsvBw = [[0,0,0],[0,0,1]]
hsvGbr = [[120,1,1],[180,1,1],[240,1,1],[300,1,1],[360,1,1]]
hsvUnknown = [[120,0.5,1],[60,0.5,1],[0,0.5,1]]
hsvCustom = [[0,1,1],[120,0.9,1],[180,0.7,1],[240,0.5,1],[300,0.3,1],[310,0,1]]

def plot_color_gradients(gradients, names):
    #For pretty latex fonts (commented out, because it does not work on some machines)
    #rc('text', usetex=True) 
    #rc('font', family='serif', serif=['Times'], size=10)
    rc('legend', fontsize=10)

    column_width_pt = 400         # Show in latex using \the\linewidth
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, axes = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
    fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)


    for ax, gradient, name in zip(axes, gradients, names):
        # Create image with two lines and draw gradient on it
        img = np.zeros((2, 1024, 3))
        for i, v in enumerate(np.linspace(0, 1, 1024)):
            img[:, i] = gradient(v)

        im = ax.imshow(img, aspect='auto')
        im.set_extent([0, 1, 0, 1])
        ax.yaxis.set_visible(False)

        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.25
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, name, va='center', ha='left', fontsize=10)

    fig.savefig('my-gradients.pdf')

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
    return start_point + ( (end_point - start_point) * value )

def transition3(value, st_pt, end_pt):
    val1 = transition(value, st_pt[0], end_pt[0])
    val2 = transition(value, st_pt[1], end_pt[1])
    val3 = transition(value, st_pt[2], end_pt[2])
    return (val1, val2, val3)

def scaling(col_list, v):
    i = 1                       #iterator
    list_len = len(col_list) - 1
    
    while(i <= list_len):
        
        if(v <= (i / (list_len) ) ):
            v = (v - ( (i - 1)/list_len) ) * list_len;
            break
            
        else:
            i += 1
            
    return(v, col_list[i-1], col_list[i])

def gradient_rgb_bw(v):
    v, rgb1, rgb2 = scaling(rgbBw, v)
    return transition3(v, rgb1, rgb2)

def gradient_rgb_gbr(v):
    v, rgb1, rgb2 = scaling(rgbGbr, v)
    return transition3(v, rgb1, rgb2)    
            
def gradient_rgb_gbr_full(v):
    v, rgb1, rgb2 = scaling(rgbGbrFull, v)
    return transition3(v, rgb1, rgb2)
    
def gradient_rgb_wb_custom(v):
    v, rgb1, rgb2 = scaling(rgbWbCustom, v)
    return transition3(v, rgb1, rgb2)

def gradient_hsv_bw(v):
    v, hsv1, hsv2 = scaling(hsvBw, v)
    h, s, v = transition3(v, hsv1, hsv2)
    return hsv2rgb(h, s, v)

def gradient_hsv_gbr(v):
    v, hsv1, hsv2 = scaling(hsvGbr, v)
    h, s, v = transition3(v, hsv1, hsv2)
    return hsv2rgb(h, s, v)
        
def gradient_hsv_unknown(v):
    v, hsv1, hsv2 = scaling(hsvUnknown, v)
    h, s, v = transition3(v, hsv1, hsv2)
    return hsv2rgb(h, s, v)

def gradient_hsv_custom(v):
    v, hsv1, hsv2 = scaling(hsvCustom, v)
    h, s, v = transition3(v, hsv1, hsv2)
    return hsv2rgb(h, s, v)
    
if __name__ == '__main__':
    def toname(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()

    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)
    
    plot_color_gradients(gradients, [toname(g) for g in gradients])
