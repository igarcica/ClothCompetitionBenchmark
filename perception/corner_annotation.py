#!/usr/bin/env python
import numpy as np
import cv2
import math
import csv

# read a colourful image
img_path = 'rulebook/towel.jpg'


img_1 = cv2.imread(img_path)
#img_1 = cv2.resize(img_1, (1280,840))

scale_percent = 40 # percent of original size
width = int(img_1.shape[1] * scale_percent / 100)
height = int(img_1.shape[0] * scale_percent / 100)
dim = (width, height)
# resize image
img_1 = cv2.resize(img_1, dim, interpolation = cv2.INTER_AREA)

# display the image
cv2.imshow('Cloth', img_1)
# read another image to display clicked colour
img_2 = img_1
cv2.imshow('Corner', img_2)

#print("debug1")
# read another image to display clicked colour
#img_2 = cv2.imread(img_path)
#img_2 = cv2.resize(img_2, (1280,840))
#cv2.imshow('Corner', img_2)

#Set variables
corner= False
corner_x = 0
corner_y = 0

def Mouse_Event(event, x, y, flags, param):
    #print("debug3")
    global corner, corner_x, corner_y
    if event == cv2.EVENT_LBUTTONDOWN:
        print("x: ", x)
        print("y: ", y)
        cv2.circle(img_2, (x, y), 10, (15,75,50), -1)
        cv2.imshow('Corner', img_2)
        corner_x = x
        corner_y = y
        corner = True
    elif event == cv2.EVENT_RBUTTONDOWN:
        print("hola")

def Vect_Event(event, x, y, flags, param):
    global corner_x, corner_y
    if event == cv2.EVENT_LBUTTONDOWN:
        if corner:
            print("x: ", x)
            print("y: ", y)
            cv2.line(img_2, (corner_x, corner_y), (x,y), (255,127,0), 5)
            cv2.imshow('Corner', img_2)
            print("Dif x: ", x - corner_x)
            print("Dif y: ", y - corner_y)
            modulo = math.sqrt(pow(x,2)+pow(y,2))
            print("modulo: ", modulo)
            data=[corner_x, corner_y, x, y]
            writer.writerow(data)
            filei.close()


# set Mouse Callback method
cv2.setMouseCallback('Cloth', Mouse_Event)
cv2.setMouseCallback('Corner', Vect_Event)

filei =open('test.csv','w')
writer=csv.writer(filei)

#print("debug5")
cv2.waitKey(0)
cv2.destroyAllWindows()


## REFS
# https://analyticsindiamag.com/real-time-gui-interactions-with-opencv-in-python/