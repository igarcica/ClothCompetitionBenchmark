#TODOs:
# - Input team name
# - Input trial number
# - Save point + vector in csv
# - Create angle tolerance based on vector

#!/usr/bin/env python
import numpy as np
import cv2
import math
import csv


def Mouse_Event(event, x, y, flags, param):
    global corner, corner_x, corner_y, vect_end_x, vect_end_y
    img_1 = param
    if event == cv2.EVENT_LBUTTONDOWN:
        print("x: ", x)
        print("y: ", y)
        cv2.circle(img_1, (x, y), 10, (15,75,50), -1)
        cv2.imshow('Cloth', img_1)
        corner_x = x
        corner_y = y
        corner = True
    elif event == cv2.EVENT_RBUTTONDOWN:
        if corner:
            print("x: ", x)
            print("y: ", y)
            cv2.line(img_1, (corner_x, corner_y), (x,y), (255,127,0), 5)
            cv2.imshow('Cloth', img_1)
            print("Dif x: ", x - corner_x)
            print("Dif y: ", y - corner_y)
            modulo = math.sqrt(pow(x,2)+pow(y,2))
            print("modulo: ", modulo)
            corner = False # To draw only one vector
            # Save corner point + origin vector point
            vect_end_x = x
            vect_end_y = y
#            data=[corner_x, corner_y, x, y]
#            writer.writerow(data)

#def Vect_Event(event, x, y, flags, param):
#    global corner_x, corner_y
#    if event == cv2.EVENT_LBUTTONDOWN:
#        if corner:
#            print("x: ", x)
#            print("y: ", y)
#            cv2.line(img_2, (corner_x, corner_y), (x,y), (255,127,0), 5)
#            cv2.imshow('Corner', img_2)
#            print("Dif x: ", x - corner_x)
#            print("Dif y: ", y - corner_y)
#            modulo = math.sqrt(pow(x,2)+pow(y,2))
#            print("modulo: ", modulo)
#            data=[corner_x, corner_y, x, y]
#            writer.writerow(data)
#            filei.close()
#

def define_groundtruth(img_path): 
    global corner, corner_x, corner_y, vect_end_x, vect_end_y

    # read a colourful image
    #img_path = 'rulebook/towel.jpg'
#    img_path = 'cloth.jpg'
    scale_percent = 40 # percent of original size
    
    #Image to select corners
    img_1 = cv2.imread(img_path)
    # resize image
    width = int(img_1.shape[1] * scale_percent / 100)
    height = int(img_1.shape[0] * scale_percent / 100)
    dim = (width, height)
    img_1 = cv2.resize(img_1, dim, interpolation = cv2.INTER_AREA)
    cv2.imshow('Cloth', img_1) 
    
    #Set internal variables
    corner = False
    corner_x = 0
    corner_y = 0
    vect_end_x = 0
    vect_end_y = 0

    param = img_1
    # set Mouse Callback method
    cv2.setMouseCallback('Cloth', Mouse_Event, param)
    #cv2.setMouseCallback('Corner', Vect_Event)
    
#    filei = open('test.csv','w')
#    writer=csv.writer(filei)
    
    cv2.waitKey(0)
    # Save points in csv
#    filei.close()
#    # Create folder for team (input team name)
#    cv2.imwrite('GT.jpg', img_1) # Save with trial number
    cv2.destroyAllWindows()

    groundtruth_img = img_1
    corner_coord = (corner_x, corner_y) 
    vect_end_coord = (vect_end_x, vect_end_y)
#Vector of corners, vector of vectors!
    return groundtruth_img, corner_coord, vect_end_coord


## Test code
#img_path = 'test/IMG_20221007_174207.jpg'
#gt_img, corner, vector_end = define_groundtruth(img_path)
#print("Corner coordinates: ", corner)
#print("Vector end coordinates: ", vector_end)
#cv2.imshow("Ground truth Image", gt_img)
#cv2.waitKey(0)


## REFS
# https://analyticsindiamag.com/real-time-gui-interactions-with-opencv-in-python/
