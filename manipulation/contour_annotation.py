#!/usr/bin/env python
import numpy as np
import cv2
import math
import csv

#px_cm_ratio = 9.25054
#px_cm_ratio_area = 85.56
#img = cv2.imread('rulebook/towel_wrinkle1.jpg')

px_cm_ratio = 11.967965888977051
px_cm_ratio_area = 143.22
img = cv2.imread('IMG_20221007_173630.jpg')

px_cm_ratio = 15.931417083740234
px_cm_ratio_area = 253.8
img = cv2.imread('IMG_20221007_174129.jpg')

px_cm_ratio = 10.700934600830077
px_cm_ratio_area = 106.08
img = cv2.imread('IMG_20221007_173646.jpg')

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
    global first, vertices, px_cm_ratio, prev_x, prev_y
    if event == cv2.EVENT_LBUTTONDOWN:
        if first:
            vertices = np.array([[x,y]])
            cv2.circle(img, (x, y), 5, (15,75,50), -1)
            cv2.imshow('Test', img)
            first = False
            prev_x = x
            prev_y = y
        else:
            #save point
            vertices = np.append(vertices, np.array([[x,y]]), axis=0)
            print(x,y)
            print(vertices)
            #cv2.circle(img, (x, y), 5, (15,75,50), -1)
            cv2.line(img,(prev_x,prev_y),(x,y),(255,0,0),3)
            cv2.imshow('Test', img)
            prev_x = x
            prev_y = y
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
# Save points in csv
filei.close()
# Create folder for team (input team name)
cv2.imwrite('rulebook/results/towel_wrinkle1.jpg', img) # Save with trial number

cv2.destroyAllWindows()


## TO DOs
#Input image path
#Get px/cm ratio from the other code
#Diccionario con expected total area, half area and quarter area --> use it to evaluate fast
#Towel Area: 4500cm2 = 45cm2, Perimeter: 280cm


## REFS
# https://analyticsindiamag.com/real-time-gui-interactions-with-opencv-in-python/
