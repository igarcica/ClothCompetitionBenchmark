
import csv
import argparse
import os
import sys
sys.path.insert(1, './px_cm/')
import px_to_cm
import corner_annotation as corner_an
import perception_scoring as scoring

tolerance = 2 # Tolerance distant in cm

# Get image with Aruco layout
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--ar_input", required=True, help="path to input image containing ArUCo layout")
ap.add_argument("-ii", "--input", required=True, help="path to input plain trial image (without markers)")
ap.add_argument("-o", "--team", required=True, type=str, default="Team", help="Team name")
ap.add_argument("-tt", "--trial", required=True, type=int, default=1, help="Trial numbber")
# number of correct corners
args = vars(ap.parse_args())


if not os.path.exists(args["team"]):
    os.mkdir(args["team"])
team = args["team"]

trial = args["trial"]


# Get px/cm ratio
print("\033[94m GETTING PIZEL/CENTIMETER RATIO \033[0m")
px_cm_ratio, px_cm_area_ratio = px_to_cm.transform_perspective(args["ar_input"])
#print("--> px to cm ratio: ", px_cm_ratio)
#print("--> px to cm AREA ratio: ", px_cm_area_ratio)

# Define ground truth corners and grasping vectors
print("\033[94m DEFINE GROUND TRUTH \033[0m")
groundtruth_img, corners_coord, vects_end_coord = corner_an.define_groundtruth(args["input"], team, trial)
print("Corner coordinates: ", corners_coord)
print("Grasping vector end coordinates: ", vects_end_coord)

# Compute error corners
print("\033[94m COMPUTE ERRORS \033[0m")
corners_error, scoring = scoring.get_corners_error(team, trial, px_cm_ratio, tolerance, args["input"])

# OK Compare corners - Error
# Compare vectors (If corner correct) - Error
# OK Ordenar puntos con sorted (de izq a derecha)


# Measured perimeter and area
print("\033[94m SAVING TRIAL RESULTS \033[0m")
results_path = team + "/perception/trial" + str(trial) + '_results.csv'
print("Saving trial ", trial, " results csv in: ", results_path, " as (px/cm ratio, px/cm area ratio, corners coordinates, vector end coordinates, corners error, scoring")
results_file =open(results_path, 'w')
writer=csv.writer(results_file)
row = [px_cm_ratio, px_cm_area_ratio, corners_coord, vects_end_coord, corners_error, scoring]#, vects_error, scoring]
writer.writerow(row)
print("Writing results in ", results_path)
# Info trial (team, trial, config, object, ...), Ratios, perimeter + area (in px and cm), error, points

#filei.close()
