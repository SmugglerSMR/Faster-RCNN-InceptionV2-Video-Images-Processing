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

def animal_get_size(lp, elephant, nb_frame, nb_count):
    # Strings to display on GUI
    elephant_size = ""
    horse_size = ""
    
    label = ""
    file = open("ProcessedStuff/labels_example.txt","a") 
    # file.write("labels = []\n")
    GSD = (ws*alt)/(lf*rw) * 100#Ground sampling distance (cm/pixel)
    la = GSD * lp
    file.write("%d,%d" % (nb_frame, nb_count))

    for i in range(1, nb_count):
        if (elephant == 1):
            label = "Elephant"
            if (la > elephant_large):
                elephant_size = "large"  
            elif (la < elephant_large and la > elephant_small):
                elephant_size = "medium"
            else:
                elephant_size = "small"
            # file.write("labels.append([%d,%d,[['%s', '%s']]])\n" % (nb_frame, 1, label, elephant_size))
            file.write(",%s,%s" % (label, elephant_size))
            # global_count = global_count+1
        else:
            label = "Horse"
            if (la > horse_large):
                horse_size = "large"  
            elif (la < horse_large and la > horse_small):
                horse_size = "medium"
            else:
                horse_size = "small"    
            file.write(",%s,%s" % (label, horse_size))
            # global_count = global_count+1
    file.write("\n")
    file.close() 
    # print("\n\nlength animal:" , la)
    # print("elep:" , elephant_size)
    # print("horse:" , horse_size)
GSD = (ws*alt)/(lf*rw) * 100#Ground sampling distance (cm/pixel)
def animal_get_size_array(lp, animals, nb_frame, nb_count, prev_count):
    # Strings to display on GUI
    animal_size = ""
    label = ""
    # Finish Comparison!!!!!!!!!!!!!
    
    if(prev_count<nb_count):
        print(lp)
        file = open("ProcessedStuff/labels_example.txt","a") 
        
        file.write("%d,%d" % (nb_frame, nb_count))

        for i in range(0, nb_count):        
            print(i)
            la = GSD * lp[i]
            if (animals[i] == 1):
                label = "Elephant"
                if (la > elephant_large):
                    animal_size = "large"  
                elif (la < elephant_large and la > elephant_small):
                    animal_size = "medium"
                else:
                    animal_size = "small"
            else:
                label = "Horse"
                if (la > horse_large):
                    animal_size = "large"  
                elif (la < horse_large and la > horse_small):
                    animal_size = "medium"
                else:
                    animal_size = "small"    
            
            file.write(",%s,%s" % (label, animal_size)) 
        file.write("\n")
        file.close() 
    else:
        fileHandle =  open("ProcessedStuff/labels_example.txt","r")
        lineList = fileHandle.readlines()
        fileHandle.close() 
        fileHandle =  open("ProcessedStuff/labels_example.txt","a")
        if len(lineList) == 0:
            fileHandle.write(lineList[len(lineList)])
        else:
            fileHandle.write(lineList[len(lineList)-1])

        #fileHandle.write("\n")
        fileHandle.close()        

