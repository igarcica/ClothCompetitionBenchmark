
import cv2
import csv
import argparse
import os
import sys
sys.path.insert(1, './px_cm/')
import px_to_cm
import corner_annotation as corner_an
import perception_scoring as scoring

tolerance = 2 # Tolerance distant in cm
resize_percent = 100 # Resizing percentage size from initial image size

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

team_trials_path = "teams_trials/"+team+"/Perception/"
output_path="teams_trials/"+team+"/Perception/scoring/"


# Get px/cm ratio
print("\033[94m GETTING PIXEL/CENTIMETER RATIO \033[0m")
aruco_img_path=team_trials_path+args["ar_input"]
px_cm_ratio, px_cm_area_ratio = px_to_cm.transform_perspective(aruco_img_path, resize_percent)


# Define ground truth corners and grasping vectors
print("\033[94m DEFINE GROUND TRUTH \033[0m")
trial_img_path=team_trials_path+args["input"]
groundtruth_img, corners_coord, vects_end_coord = corner_an.define_groundtruth(trial_img_path, output_path, team, trial, resize_percent)
print("Corner coordinates: ", corners_coord)
print("Grasping vector end coordinates: ", vects_end_coord)

# Resize image (too small)
width = int(groundtruth_img.shape[1] * 300 / 100)
height = int(groundtruth_img.shape[0] * 300 / 100)
dim = (width, height)
img = cv2.resize(groundtruth_img, dim, interpolation = cv2.INTER_AREA)
output_img_file=output_path+"trial"+str(trial)+"_results.png"
cv2.imwrite(output_img_file, img) # Save with trial number
cv2.imshow("Result image", img)
cv2.waitKey(0)
output_img_file=output_path+"trial"+str(trial)+"_gt.jpg"
cv2.imwrite(output_img_file, img) # Save with trial number


# Compute error corners
print("\033[94m COMPUTE ERRORS \033[0m")
plain_img_path=team_trials_path+args["input"] # Plain image path to show results
results_img, corners_error, scoring = scoring.get_corners_error(plain_img_path, team_trials_path, output_path, team, trial, px_cm_ratio, tolerance, resize_percent)

# Image to select corners
print("Show image with results of trial")
#img = cv2.imread(results_img)
img = results_img
# Resize image (too small)
scale_percent = resize_percent # percent of original size
width = int(results_img.shape[1] * 300 / 100)
height = int(results_img.shape[0] * 300 / 100)
dim = (width, height)
img = cv2.resize(results_img, dim, interpolation = cv2.INTER_AREA)
output_img_file=output_path+"trial"+str(trial)+"_results.png"
cv2.imwrite(output_img_file, img) # Save with trial number
cv2.imshow("Result image", img)
cv2.waitKey(0)


# Measured perimeter and area
print("\033[94m SAVING TRIAL RESULTS \033[0m")
results_path = output_path + "trial" +str(trial) + "_results.csv"
#results_path = team + "/perception/trial" + str(trial) + '_results.csv'
print("Saving trial ", trial, " results csv in: ", results_path, " as (px/cm ratio, px/cm area ratio, corners coordinates, vector end coordinates, corners error, scoring")
results_file =open(results_path, 'w')
writer=csv.writer(results_file)
row = [px_cm_ratio, px_cm_area_ratio, corners_coord, vects_end_coord, corners_error, scoring]#, vects_error, scoring]
writer.writerow(row)
print("Writing results in ", results_path)
# Info trial (team, trial, config, object, ...), Ratios, perimeter + area (in px and cm), error, points

#filei.close()

##TODO
# OK Compare corners - Error
# Compare vectors (If corner correct) - Error
# OK Ordenar puntos con sorted (de izq a derecha)
