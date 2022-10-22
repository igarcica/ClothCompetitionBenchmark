#TODOs:
# OK - Save point + vector in csv
# - Create angle tolerance based on vector

#!/usr/bin/env python
import numpy as np
import cv2
import math
import csv
from scipy.spatial import distance


def Mouse_Event(event, x, y, flags, param):
    global corner, corner_x, corner_y, vect_end_x, vect_end_y, corner_coord, vect_end_coord
    img = param
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x, y), 5, (0,0,255), -1)
        cv2.imshow('Define groundtruth', img)
        corner_x = x
        corner_y = y
        corner = True
        #print("Corner: (", x, ",", y, ")")
    elif event == cv2.EVENT_RBUTTONDOWN:
        if corner:
            cv2.line(img, (corner_x, corner_y), (x,y), (255,127,0), 2)
            cv2.circle(img, (corner_x, corner_y), 5, (0,0,255), -1)
            cv2.imshow('Define groundtruth', img)
            corner = False # To draw only one vector
            vect_end_x = x
            vect_end_y = y
            #print("Origin: (", corner_x, ",", corner_y, "), End: (", vect_end_x, ",", vect_end_y, ")")
            #print("Dif x: (", x-corner_x, ", ", y-corner_y, ")")
            modulo = math.sqrt(pow(x,2)+pow(y,2))
            #print("Module: ", modulo)
            data=[corner_x, corner_y, vect_end_x, vect_end_y]
            writer.writerow(data)
            corner_coord.append([corner_x, corner_y]) 
            vect_end_coord.append([vect_end_x, vect_end_y])
#            define_grasp_approach_range(img, corner_x, corner_y, vect_end_x, vect_end_y)


def define_grasp_approach_range(img, corner_x, corner_y, vector_end_x, vector_end_y):
    corner = np.array((corner_x, corner_y))
    vector = np.array((vector_end_x, vector_end_y))
    dist = distance.euclidean(corner, vector)
    range1 = dist/math.sqrt(2)
    print(range1)

#    dif_x=vect_end_x-corner_x
#    range1_x = corner_x+dif_x
#    cv2.circle(img, (range1_x, corner_y), 5, (255,0,0), -1)
#
#    dif_y=vect_end_y-corner_y
#    range2_y = corner_y+dif_y
#    cv2.circle(img, (corner_x, range2_y), 5, (255,0,0), -1)
#

    range1_x = math.sin(45)*math.cos(45)*dist
    range1_y = math.cos(45)*math.sin(45)*dist
    print(range1_x, range1_y)
    cv2.circle(img, (int(range1_x), int(range1_y)), 5, (255,0,0), -1)

    cv2.imshow('Define groundtruth', img)
    cv2.waitKey(0)


def define_groundtruth(img_path, output_path, team, trial, resize_percent):
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
    print("Reading plain image of trial ", trial, " from: ", img_path)
    img = cv2.imread(img_path)

    # Resize image to fit the screen
    scale_percent = resize_percent # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    cv2.imshow('Define groundtruth', img) 

    # Create file to save results
#    output_csv_file = team + "/perception/trial" + str(trial) + "_gt.csv"
    output_csv_file=output_path+"trial"+str(trial)+"_gt.csv"
    filei =open(output_csv_file,'w')
    writer=csv.writer(filei)

    # set Mouse Callback method
    param = img
    cv2.setMouseCallback('Define groundtruth', Mouse_Event, param)
    
    print("\033[95m Action required! \033[0m Please, define ground truth for corners and their grasping approach vectors")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Save points in csv
    filei.close()
#    output_img_file=output_folder + "/perception/trial" + str(trial) + "_gt.jpg"
    output_img_file=output_path+"trial"+str(trial)+"_gt.jpg"
    cv2.imwrite(output_img_file, img) # Save with trial number
    print("Saving ground truth image in: ", output_img_file, " and corner/end vector coordinates in ", output_csv_file)

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
