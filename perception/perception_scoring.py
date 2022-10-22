## CORNERS
#OK Get GT point (csv)
#OK Get team point (csv)
#OK Measure difference
# Ensure that the corners coincide!
# Transform to cm
# Based on tolerance (1cm), compute points

## VECTOR
# If corner correct, then:
# Get tolerance angle --> como?
# Get team vector (csv)
# Measure if team vector is inside tolerance --> como?
# If it is inside, compute points
# producto vectorial

# Create team folder
# Save GT + team images
# Save name team + n trial + points

import sys
import getopt
import cv2
import numpy as np
from scipy.spatial import distance
#import pandas as pd
import csv


def sort_corners(corners):
    y_order = sorted(corners, key=lambda corners: corners[1])
    x1_order = y_order[:2]
    x1_order = sorted(x1_order, key=lambda x1_order: x1_order[0])
    x2_order = y_order[2:4]
    x2_order = sorted(x2_order, key=lambda x2_order: x2_order[0])

    return [x1_order[0], x1_order[1], x2_order[0], x2_order[1]]

def save_results(img_path, gt_corner, team_corner):
    # Create image with results
    print("\033[94m SHOWING RESULTS \033[0m")
    # Plain image
    print("Reading plain image of trial ", trial, " from: ", img_path)
    img = cv2.imread(img_path)
    # Read csvs files + plain image
    # Paint GT and detected results
    cv2.circle(img, (gt_corner[0], gt_corner[1]), 3, (15,75,50), -1) #GT color?
    cv2.circle(img, (team_corner[0], team_corner[1]), 3, (15,75,50), -1) #Team color? Red?
    cv2.imshow('Perception results', img)
    cv2.waitKey(0)
    output_img_file=output_folder + "/perception/trial" + str(trial) + "_results.jpg"
    cv2.imwrite(output_img_file, img) # Save with trial number

#def get_grasping_v_error(img_path, output_path, team, trial, px_cm_ratio, tolerance):
#
#    points = 0
#    corners_error = []
#
#    img = cv2.imread(img_path)
#    # Resize image to fit the screen
#    scale_percent = 40 # percent of original size
#    width = int(img.shape[1] * scale_percent / 100)
#    height = int(img.shape[0] * scale_percent / 100)
#    dim = (width, height)
#    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
#
#    # Read CSV files with groundtruth and results
#    gt_file = csv.reader(open(team + "/perception/trial" + str(trial) + '_gt.csv'))
#    team_file = csv.reader(open(team + "/perception/trial" + str(trial) + '.csv'))
#    gt_data = []
#    team_data = []
#    for rows in gt_file:
#        gt_data.append(rows)
#    for rows in team_file:
#        team_data.append(rows)
#
#    team_data = sort_corners(team_data) # Order team corners as topl, topr, botl, botr
#
#    n_corners_gt = len(gt_data)
#    n_corners_team = len(team_data)

def get_corners_error(img_path,input_path, output_path, team, trial, px_cm_ratio, tolerance, resize_percent):

    points = 0
    corners_error = []

    # Plain image to show results
    img = cv2.imread(img_path)
    # Resize image to fit the screen
    scale_percent = resize_percent # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    # Read CSV files with groundtruth and results
    team_corners_path = input_path+"/detection_" + str(trial) + "_results.csv"
    gt_corners_path = output_path+"trial"+str(trial)+"_gt.csv"
    gt_file = csv.reader(open(gt_corners_path))
    team_file = csv.reader(open(team_corners_path))
    gt_data = []
    team_data = []
    for rows in gt_file:
        gt_data.append(rows)
    for rows in team_file:
        team_data.append(rows)

    team_data = sort_corners(team_data) # Order team corners as topl, topr, botl, botr

    n_corners_gt = len(gt_data)
    n_corners_team = len(team_data)

    # Check if number of corners detected coincides
#    if n_corners_gt == n_corners_team:
#        for i in range(n_corners_gt):
#            gt_corner = np.array((int(gt_data[i][0]), int(gt_data[i][1])))
#            team_corner = np.array((int(team_data[i][0]), int(team_data[i][1])))
#            #dist = np.linalg.norm(a-b)
#            dist = distance.euclidean(gt_corner, team_corner)
#            dist_cm = dist/px_cm_ratio
#            if dist_cm < tolerance:
#                points += 1
#                print("Corner ", i+1, " is correct = +1 point.  Error=", dist_cm)
#            else:
#                print("Error is > than tolerance! Distance between corners in cm is: ", dist_cm)
#            corners_error.append(dist_cm)
#
#            # Paint GT and detected results
#            cv2.circle(img, (gt_corner[0], gt_corner[1]), 10, (15,75,50), -1) #GT color?
#            cv2.circle(img, (team_corner[0], team_corner[1]), 10, (0,0,255), -1) #Team color? Red?
#            cv2.imshow('Perception results', img)
#            cv2.waitKey(0)
#    elif n_corners_gt > n_corners_team:
#        print("Not all corners detected!")
#        #Que hacer??? editar csv a mano?
#    elif n_corners_gt < n_corners_team:
#    print("Detected more number of corners than required")
#    Compare GT and team points and get error from closest ones

    if n_corners_gt == n_corners_team:
        print("Same number of corners detected")
    elif n_corners_gt > n_corners_team:
        print("Not all corners detected!")
    elif n_corners_gt < n_corners_team:
        print("Detected more number of corners than required")

    print(n_corners_gt, " corners in GT. ", n_corners_team, " detected corners")
    for i in range(n_corners_gt):
        print("Getting error of next corner")
        prev_dist =100000
        for j in range(n_corners_team):
            gt_corner = np.array((int(gt_data[i][0]), int(gt_data[i][1])))
            team_corner = np.array((int(team_data[j][0]), int(team_data[j][1])))
            dist = distance.euclidean(gt_corner, team_corner)
            #print("Team corner ", j, "error (in px):", dist) 
            if dist < prev_dist:
                prev_dist = dist
                n_corner = j
        # Score closest points
        gt_corner = np.array((int(gt_data[i][0]), int(gt_data[i][1])))
        team_corner = np.array((int(team_data[n_corner][0]), int(team_data[n_corner][1])))
        dist = distance.euclidean(gt_corner, team_corner)
        dist_cm = dist/px_cm_ratio
        if dist_cm < tolerance:
#            success=True
            points += 1
            print("Corner ", n_corner+1, " is correct = +1 point.  Error=", dist_cm)
        else:
#            success=False
            print("Corner ", n_corner+1, " error is > than tolerance! Distance between closest corners in cm is: ", dist_cm)
        corners_error.append(dist_cm)

        # Paint GT and detected results
        cv2.circle(img, (gt_corner[0], gt_corner[1]), 5, (255,127,0), -1) #GT color?
        cv2.circle(img, (team_corner[0], team_corner[1]), 5, (0,0,255), -1) #Team color? Red?
#        text_string = str(round(dist_cm))
#        cv2.putText(img, text_string, (gt_corner[0], gt_corner[1]+50), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(15,75,50))
        cv2.imshow('Perception results', img)
        cv2.waitKey(0)

        # Save results
        output_img_file=output_path+"trial"+str(trial)+"_results.png"
        cv2.imwrite(output_img_file, img) # Save with trial number

        cv2.imshow("Result image", img)
        cv2.waitKey(0)



    return img, corners_error, points

## Test code
#team = 'team2'
#trial = 1000
#px_cm_ratio = 9
#tolerance = 2 # in cm
#img_path
#resize_percent=100
#print("hola")
#corners_errors, points = get_corners_error(team, trial, px_cm_ratio, tolerance, img_path, resize_percent)
#
#print("Corners errors (in cm): ", corners_errors)
#print("Total points: ", points)




    # Read team csv + save corners in matrix
    # Sort team corners

    # Read GT csv

    #Compute difference between corners (check number of corners!)


## NOTEs
# To correct: If there is a false corners with which one do we relate it? (e.g. it could be that two detected corners are below tolerance of the same point)
