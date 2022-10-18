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

tolerance = 1 # in cm
points = 0

def sort_corners(corners):
    y_order = sorted(corners, key=lambda corners: corners[1])
    x1_order = y_order[:2]
    x1_order = sorted(x1_order, key=lambda x1_order: x1_order[0])
    x2_order = y_order[2:4]
    x2_order = sorted(x2_order, key=lambda x2_order: x2_order[0])

    return [x1_order[0], x1_order[1], x2_order[0], x2_order[1]]

#def get_px_cm_ratio():
#    px_cm_file = csv.reader(open(px_cm_csv))
#    for rows in px_cm_file:
#        px_cm_team = rows
#        print("px/cm ratio: ", px_cm_team)
#
def get_error(team, trial, px_cm_ratio):
    global points

    print(team + "/trial" + str(trial) + '_gt.csv')

    gt_file = csv.reader(open(team + "/trial" + str(trial) + '_gt.csv'))
    team_file = csv.reader(open(team + "/trial" + str(trial) + '.csv'))
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
    if n_corners_gt == n_corners_team:
        for i in range(n_corners_gt):
            gt_corner = np.array((int(gt_data[i][0]), int(gt_data[i][1])))
            team_corner = np.array((int(team_data[i][0]), int(team_data[i][1])))
            #dist = np.linalg.norm(a-b)
            dist = distance.euclidean(gt_corner, team_corner)
            dist_cm = dist/px_cm_ratio
            if dist_cm < tolerance:
                points += 1
                print("Points: ", points)
            else:
                print("Distance of points in cm is: ", dist_cm)
                print("Error is > than tolerance!")
    else:
        print("Not all corners detected!")
        #Que hacer??? editar csv a mano?


#def main(argv):
#   global gt_csv, team_csv
#   try:
#      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
#   except getopt.GetoptError:
#      print('perception.py -i <gt_csv> -o <team_csv>')
#      sys.exit(2)
#   for opt, arg in opts:
#      if opt == '-h':
#         print('perception.py -i <gt_csv> -o <team_csv>')
#         sys.exit()
#      elif opt in ("-i", "--ifile"):
#         gt_csv = arg
#      elif opt in ("-o", "--ofile"):
#         team_csv = arg
#   print('File with ground truth is "', gt_csv)
#   print('File with team s result is "', team_csv)
#
#
#if __name__=="__main__":
#    main(sys.argv[1:])
##    get_error()
#

## Test code
#team = 'team2'
#trial = 1000
#px_cm_ratio = 9
#get_error(team, trial, px_cm_ratio)




    # Read team csv + save corners in matrix
    # Sort team corners

    # Read GT csv

    #Compute difference between corners (check number of corners!)


