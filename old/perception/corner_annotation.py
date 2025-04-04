#TODOs:
# OK - Save point + vector in csv
# - Create angle tolerance based on vector

#!/usr/bin/env python
import numpy as np
import cv2
import math
import csv

activate_print = False

def print_info(activate, arg1, arg2="", arg3="", arg4="", arg5="", arg6="", arg7="", arg8="", arg9="", arg10=""):
    if(activate):
        print(str(arg1) + str(arg2) + str(arg3) + str(arg4) + str(arg5) + str(arg6) + str(arg7) + str(arg8) + str(arg9) + str(arg10))

def Mouse_Event(event, x, y, flags, param):
    global corner, corner_x, corner_y, vect_end_x, vect_end_y, corner_coord, vect_end_coord, results
    
    gt_img = param[0]
    trial_img = param[1]
    px_cm = param[2]
    corner_tolerance_error = px_cm*2 # How many pixel for 1cm
    if event == cv2.EVENT_LBUTTONDOWN:
        #cv2.circle(gt_img, (x, y), 5, (255,0,0), -1) # Draw corner 
        cv2.circle(gt_img, (x, y), int(corner_tolerance_error), (255,127,0), 2) # Draw corner detection tolerance #(15,75,50) 
        cv2.circle(trial_img, (x, y), int(corner_tolerance_error), (255,127,0), 2) # Draw corner detection tolerance #(15,75,50) 
        cv2.imshow('Define groundtruth', gt_img)
        corner_x = x
        corner_y = y
        corner = True
        #print("Corner: (", x, ",", y, ")")
    elif event == cv2.EVENT_RBUTTONDOWN:
        if corner:
            #cv2.line(gt_img, (corner_x, corner_y), (x,y), (255,0,0), 2)
            #cv2.circle(img, (corner_x, corner_y), 3, (15,75,50), -1)
            cv2.imshow('Define groundtruth', gt_img)
            corner = False # To draw only one vector
            vect_end_x = x
            vect_end_y = y
            print_info(activate_print, "Origin: (", corner_x, ",", corner_y, "), End: (", vect_end_x, ",", vect_end_y, ")")
            print_info(activate_print, "Dif x: (", x-corner_x, ", ", y-corner_y, ")")
            modulo = math.sqrt(pow(x,2)+pow(y,2))
            print_info(activate_print, "Module: ", modulo)
            # data=[corner_x, corner_y, vect_end_x, vect_end_y]
            # writer.writerow(data)
            corner_coord.append([corner_x, corner_y]) 
            vect_end_coord.append([vect_end_x, vect_end_y])
            results.append([corner_x, corner_y, vect_end_x, vect_end_y])

            dir_x = x-corner_x
            dir_y = y-corner_y
            mid_point_x = corner_x+(dir_x/2)
            mid_point_y = corner_y+(dir_y/2)
            print_info(activate_print, "MID POINTS: ", mid_point_x, " / ", mid_point_y)
            # p10 = mid_point_x + (dir_y/2)
            # p11 = mid_point_x - (dir_y/2)
            # p20 = mid_point_y + (dir_x/2)
            # p21 = mid_point_y - (dir_x/2)
            p10 = mid_point_x - (dir_y/2)
            p11 = mid_point_y + (dir_x/2)
            p20 = mid_point_x + (dir_y/2)
            p21 = mid_point_y - (dir_x/2)
            print_info(activate_print, "PONTS: ", p10, " / ", p11, " / ", p20, " / ", p21)
            ## GT plain image
            cv2.line(gt_img, (corner_x, corner_y), (int(p10),int(p11)), (255,127,0), 2)
            cv2.line(gt_img, (corner_x, corner_y), (int(p20),int(p21)), (255,127,0), 2)
            ## Trial image
            cv2.line(trial_img, (corner_x, corner_y), (int(p10),int(p11)), (255,127,0), 2)
            cv2.line(trial_img, (corner_x, corner_y), (int(p20),int(p21)), (255,127,0), 2)
            # cv2.circle(img, (int(p10), int(p20)), 3, (15,75,50), -1)
            # cv2.circle(img, (int(p11), int(p21)), 3, (15,75,50), -1)
            cv2.imshow('Define groundtruth', gt_img)



            # if(dir_x>dir_y):



#def define_groundtruth(img_path, output_path, team, trial, resize_percent, px_cm_ratio):
def define_groundtruth(gt_img, trial_img, output_path, team, trial, px_cm_ratio):
    global corner, corner_x, corner_y, vect_end_x, vect_end_y, corner_coord, vect_end_coord, writer, results
   
    #Set internal variables
    corner = False
    corner_x = 0
    corner_y = 0
    vect_end_x = 0
    vect_end_y = 0
    corner_coord = []
    vect_end_coord = []
    results = []

    # # Image to select corners
    # #print("Reading plain image of trial ", trial, " from: ", img_path)
    # print("\033[94m Reading image: \033[0m", img_path)
    # img = cv2.imread(img_path)
    # # Resize image to fit the screen
    # scale_percent = resize_percent # percent of original size
    # width = int(img.shape[1] * scale_percent / 100)
    # height = int(img.shape[0] * scale_percent / 100)
    # dim = (width, height)
    # img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    cv2.imshow('Define groundtruth', gt_img) 

    # # Create file to save results
    # # output_csv_file = team + "/perception/trial" + str(trial) + "_gt.csv"
    # output_csv_file=output_path+"trial"+str(trial)+"_gt.csv"
    # filei =open(output_csv_file,'w')
    # writer=csv.writer(filei)

    # set Mouse Callback method
    param = [gt_img, trial_img, px_cm_ratio]
    cv2.setMouseCallback('Define groundtruth', Mouse_Event, param)
    
    print("\033[95m Action required! \033[0m Please, define ground truth for corners and their grasping approach vectors")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("\033[96m Ended defining GT corners \033[0m")

    # # Save points in csv
    # filei.close()
    # #output_img_file=output_folder + "/perception/trial" + str(trial) + "_gt.jpg"
    # output_img_file=output_path+"trial"+str(trial)+"_gt.jpg"
    # cv2.imwrite(output_img_file, img) # Save with trial number
    # print("Saving ground truth image in: ", output_img_file, " and corner/end vector coordinates in ", output_csv_file)

    # Vector of corners, vector of vectors!
    groundtruth_image = gt_img
    trial_image = trial_img
    
    return groundtruth_image, trial_image, results, corner_coord, vect_end_coord


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
