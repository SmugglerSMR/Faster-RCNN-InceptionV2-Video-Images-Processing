# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 13:12:23 2018

@author: kaing
"""
import math

# Some Camera Propertieis and Constants
lf = 24  # focal length of camera (mm)
ws = 32  #sensor width (mm)
alt = 8  #altitude of camera (m)
rw = 910 #image width in pixels 
rh = 480 #image height in pixels
lp = 95#length of animal in pixels
y = 165 #y position of the animal

# Dimensions of adult sized animals
elephant_large = 500
elephant_small = 200
horse_large = 200
horse_small = 100

# Set animal for detection, 0 = Horse, 1 = Elephant
elephant = 0
global global_count
global_count = 1

def animal_get_size(lp, elephant, nb_frame):
    # Strings to display on GUI
    elephant_size = ""
    horse_size = ""
    
    label = ""
    file = open("ProcessedStuff/labels_example.txt","a") 
    # file.write("labels = []\n")
    GSD = (ws*alt)/(lf*rw) * 100#Ground sampling distance (cm/pixel)
    la = GSD * lp

    if (elephant == 1):
        label = "Elephant"
        if (la > elephant_large):
            elephant_size = "large"  
        elif (la < elephant_large and la > elephant_small):
            elephant_size = "medium"
        else:
            elephant_size = "small"
        # file.write("labels.append([%d,%d,[['%s', '%s']]])\n" % (nb_frame, 1, label, elephant_size))
        file.write("%d,%d,%s,%s\n" % (nb_frame, 6, label, elephant_size))
        # global_count = global_count+1
    else:
        label = "Horse"
        if (la > horse_large):
            horse_size = "large"  
        elif (la < horse_large and la > horse_small):
            horse_size = "medium"
        else:
            horse_size = "small"    
        file.write("%d,%d,%s,%s\n" % (nb_frame, 6, label, horse_size))
        # global_count = global_count+1
    file.close() 
    # print("\n\nlength animal:" , la)
    # print("elep:" , elephant_size)
    # print("horse:" , horse_size)



