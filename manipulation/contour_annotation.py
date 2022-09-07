#!/usr/bin/env python
import numpy as np
import cv2
import math
import csv

px_cm_ratio = 9.25054
px_cm_ratio_area = 85.56

# read a colourful image
img = cv2.imread('rulebook/towel.jpg')
print("Image dim: ", img.shape)
scale_percent = 40 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
# resize image
img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

cv2.imshow('Test', img)
#print("debug2")

#Set variables
first = True
#vertices = np.array([[]])
#print(vertices)

def Vect_Event(event, x, y, flags, param):
    global first, vertices, px_cm_ratio
    if event == cv2.EVENT_LBUTTONDOWN:
        if first:
            vertices = np.array([[x,y]])
            first = False
        else:
            #save point
            vertices = np.append(vertices, np.array([[x,y]]), axis=0)
            print(x,y)
            print(vertices)
            cv2.circle(img, (x, y), 5, (15,75,50), -1)
            cv2.imshow('Test', img)
    if event == cv2.EVENT_RBUTTONDOWN:
        print("hola")
        pts = vertices.reshape((-1,1,2))
        cv2.polylines(img, [pts], True, (0,0,255), 3)
        cv2.imshow('Test', img)
        print("Area (px): ", cv2.contourArea(vertices))
        print("Area (cm): ", cv2.contourArea(vertices)/px_cm_ratio_area)
        print("Perimeter (pc): ", cv2.arcLength(vertices, True))
        print("Perimeter (cm): ", cv2.arcLength(vertices, True)/px_cm_ratio)
        #Stop getting vertices
        #Join last point with initial

#Should be in code for Unfolding/Folding
#pts = np.array( [[10,50], [400,50], [90,200], [50,500]], np.int32)# Let's now reshape our points in form  required by polylines
#pts = pts.reshape((-1,1,2))
#cv2.polylines(image, [pts], True, (0,0,255), 3)

# set Mouse Callback method
cv2.setMouseCallback('Test', Vect_Event)

filei =open('test.csv','w')
writer=csv.writer(filei)

#print("debug5")
cv2.waitKey(0)
cv2.destroyAllWindows()


## TO DOs
#Input image path
#Get px/cm ratio from the other code
#Diccionario con expected total area, half area and quarter area --> use it to evaluate fast
#Towel Area: 4500cm2 = 45cm2, Perimeter: 280cm


## REFS
# https://analyticsindiamag.com/real-time-gui-interactions-with-opencv-in-python/
