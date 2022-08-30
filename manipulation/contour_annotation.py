#!/usr/bin/env python
import numpy as np
import cv2
import math
import csv

# read a colourful image
img_1 = cv2.imread('cloth.jpg')
img_1 = cv2.resize(img_1, (1280,840))
#img_1 = cv2.resize(img_1, (320,210))
# display the image
cv2.imshow('Cloth', img_1)

#print("debug1")
# read another image to display clicked colour
img_2 = cv2.imread('cloth2.jpg')
img_2 = cv2.resize(img_2, (1280,840))
cv2.imshow('Test', img_2)
#print("debug2")

#Set variables
first = True
#vertices = np.array([[]])
#print(vertices)

def Vect_Event(event, x, y, flags, param):
    global first, vertices
    if event == cv2.EVENT_LBUTTONDOWN:
        if first:
            vertices = np.array([[x,y]])
            first = False
        else:
            #save point
            vertices = np.append(vertices, np.array([[x,y]]), axis=0)
            print(x,y)
            print(vertices)
            cv2.circle(img_2, (x, y), 5, (15,75,50), -1)
            cv2.imshow('Test', img_2)
    if event == cv2.EVENT_RBUTTONDOWN:
        print("hola")
        pts = vertices.reshape((-1,1,2))
        cv2.polylines(img_2, [pts], True, (0,0,255), 3)
        cv2.imshow('Test', img_2)
        print(cv2.contourArea(vertices))
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


## REFS
# https://analyticsindiamag.com/real-time-gui-interactions-with-opencv-in-python/
