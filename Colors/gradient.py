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
# Lista punktów tworzących odcinki na stożku
hsvBw = [[0,0,0],[0,0,1]]
hsvGBR = [[120,1,1],[180,1,1],[240,1,1],[300,1,1],[360,1,1]]
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

def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return (r, g, b)

def hsv2rgbw(h, s, v):   # (hue, sat, val)
    h = h % 360.0   # color scale is a circle
    if v == 0:
        return (0, 0, 0)
    h = h / 60
    section = h // 1
    fraction = h - section
    Mid_odd = v * (1-(s*fraction))
    Mid_even = v * (1-s+(s*fraction))
    m = v - v*s # m - amount to match value
    if section == 0:
        return v, Mid_even, m
    elif section == 1:
        return Mid_odd, v, m
    elif section == 2:
        return m, v, Mid_even
    elif section == 3:
        return m, Mid_odd, v
    elif section == 4:
        return Mid_even, m, v
    elif section == 5:
        return v, m, Mid_odd
    return (-1, -1, -1)


def transition(value, start_point, end_point):
    return start_point + (end_point - start_point)*value

def transition3(value, s, e):
    r = transition(value, s[0], e[0])
    g = transition(value, s[1], e[1])
    b = transition(value, s[2], e[2])
    return (r, g, b)

def scaling(col_list, v):
    i = 1
    list_len = len(col_list) - 1
    while(i <= list_len):
        if(v <= (i / (list_len) ) ):
            v = (v - ((i - 1)/list_len) ) * list_len;
            break
        else:
            i = i + 1
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
    v, rgb1, rgb2 = scaling(gbrWbCustom, v)
    return transition3(v, rgb1, rgb2)

def gradient_hsv_bw(v):
    v, hsv1, hsv2 = scaling(hsvBw, v)
    h, s, v = transition3(v, hsv1, hsv2)
    return hsv2rgbw(h, s, v)

def gradient_hsv_gbr(v):
    v, hsv1, hsv2 = scaling(hsvGbr, v)
    h, s, v = transition3(v, hsv1, hsv2)
    return hsv2rgbw(h, s, v)
        
def gradient_hsv_unknown(v):
    v, hsv1, hsv2 = scaling(hsvUnknown, v)
    h, s, v = transition3(v, hsv1, hsv2)
    return hsv2rgbw(h, s, v)

def gradient_hsv_custom(v):
    v, hsv1, hsv2 = scaling(hsvCustom, v)
    h, s, v = transition3(v, hsv1, hsv2)
    return hsv2rgbw(h, s, v)
    
if __name__ == '__main__':
    def toname(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()

    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)
    
    plot_color_gradients(gradients, [toname(g) for g in gradients])
