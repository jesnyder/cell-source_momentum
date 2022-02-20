import os
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random

from a0001_admin import retrieve_path
from a0001_admin import retrieve_format

def find_color(num):
    """

    """

    # print('finding color')

    #colorTransparency = retrieve_ref('scatterTransparency')
    colorTransparency = 0.8

    colorOrange = [240/255, 83/255, 35/255]
    colorPurple = [23/255, 27/255, 96/255]
    colorBlueDark = [0/255, 153/255, 216/255]
    colorBlueLight = [0/255, 188/255, 231/255]
    colorGray = [233/255, 225/255, 223/255]

    variant = random.randint(-50,50)
    variant = variant/50
    variant_change_strong = 0.1
    variant_change_weak = 0.1

    colorMarker = colorOrange
    colorEdge = colorPurple

    for j in range(len(colorMarker)):

        if num%4 == 0:
            if j == 0:  colorMarker[j] = colorOrange[0] + variant*variant_change_weak
            if j == 1:  colorMarker[j] = colorOrange[1] - variant*variant_change_strong
            if j == 2:  colorMarker[j] = colorOrange[2] + variant*variant_change_strong

        if num%4 == 1:
            if j == 0:  colorMarker[j] = colorBlueDark[0] - variant*variant_change_strong
            if j == 1:  colorMarker[j] = colorBlueDark[1] + variant*variant_change_strong
            if j == 2:  colorMarker[j] = colorBlueDark[2] + variant*variant_change_weak

        if num%4 == 2:
            if j == 0:  colorMarker[j] = colorBlueLight[0] - variant*variant_change_strong
            if j == 1:  colorMarker[j] = colorBlueLight[1] + variant*variant_change_strong
            if j == 2:  colorMarker[j] = colorBlueLight[2] + variant*variant_change_weak

        if num%4 == 3:
            if j == 0:  colorMarker[j] = colorPurple[0] - variant*variant_change_strong
            if j == 1:  colorMarker[j] = colorPurple[1] + variant*variant_change_strong
            if j == 2:  colorMarker[j] = colorPurple[2] + variant*variant_change_weak

    for ii in range(len(colorMarker)):
        colorMarker[ii] = round(colorMarker[ii],4)
        if colorMarker[ii] > 1: colorMarker[ii] = 1
        elif colorMarker[ii] < 0: colorMarker[ii] = 0

    colorEdge[j] = 0.85*colorMarker[j]

    """
    print('colorMarker = ')
    print(colorMarker)

    print('colorEdge = ')
    print(colorEdge)

    print('scatterTransparency = ' + str(scatterTransparency))
    """

    return(colorMarker, colorEdge, colorTransparency)
