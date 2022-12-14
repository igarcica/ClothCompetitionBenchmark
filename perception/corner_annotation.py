#TODOs:
# - Save point + vector in csv
# - Create angle tolerance based on vector

#!/usr/bin/env python
import numpy as np
import cv2
import math
import csv


def Mouse_Event(event, x, y, flags, param):
    global corner, corner_x, corner_y, vect_end_x, vect_end_y, corner_coord, vect_end_coord
    img = param
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x, y), 10, (15,75,50), -1)
        cv2.imshow('Define groundtruth', img)
        corner_x = x
        corner_y = y
        corner = True
        print("Corner: (", x, ",", y, ")")
    elif event == cv2.EVENT_RBUTTONDOWN:
        if corner:
            cv2.line(img, (corner_x, corner_y), (x,y), (255,127,0), 5)
            cv2.imshow('Define groundtruth', img)
            corner = False # To draw only one vector
            vect_end_x = x
            vect_end_y = y
            print("Origin: (", corner_x, ",", corner_y, "), End: (", vect_end_x, ",", vect_end_y, ")")
            print("Dif x: (", x-corner_x, ", ", y-corner_y, ")")
            modulo = math.sqrt(pow(x,2)+pow(y,2))
            print("Module: ", modulo)
            data=[corner_x, corner_y, vect_end_x, vect_end_y]
            writer.writerow(data)
            corner_coord.append([corner_x, corner_y]) 
            vect_end_coord.append([vect_end_x, vect_end_y])


def define_groundtruth(img_path, output_folder, trial):
    global corner, corner_x, corner_y, vect_end_x, vect_end_y, corner_coord, vect_end_coord, writer
    
    #Set internal variables
    corner = False
    corner_x = 0
    corner_y = 0
    vect_end_x = 0
    vect_end_y = 0
    corner_coord = []
    vect_end_coord = []

    # Image to select corners
    img = cv2.imread(img_path)
    # Resize image to fit the screen
    scale_percent = 40 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    cv2.imshow('Define groundtruth', img) 
    

    # Create file to save results
    filei =open(output_folder + "/trial" + str(trial) + '_gt.csv','w')
    writer=csv.writer(filei)

    # set Mouse Callback method
    param = img
    cv2.setMouseCallback('Define groundtruth', Mouse_Event, param)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Save points in csv
    filei.close()
    # Create folder for team (input team name)
    cv2.imwrite(output_folder + "/trial" + str(trial) + "_gt.jpg", img) # Save with trial number

#Vector of corners, vector of vectors!
    groundtruth_img = img

    return groundtruth_img, corner_coord, vect_end_coord


## Test code
#img_path = 'test/IMG_20221007_174207.jpg'
#output_folder = 'team2'
#trial = 1
#gt_img, corners, vectors_end = define_groundtruth(img_path, output_folder, trial)
#print("Corner coordinates: ", corners)
#print("Vector end coordinates: ", vectors_end)
#cv2.imshow("Ground truth Image", gt_img)
#cv2.waitKey(0)


## REFS
# https://analyticsindiamag.com/real-time-gui-interactions-with-opencv-in-python/
