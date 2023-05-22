
import cv2
import csv
import argparse
import os
import sys
import numpy as np
sys.path.insert(1, './px_cm/')
import px_to_cm
import corner_annotation as corner_an
import perception_scoring as scoring

tolerance = 2 # Tolerance distant in cm
resize_percent = 300 # Resizing percentage size from initial image size

test = False
activate_print = True

# Get image with Aruco layout
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--ar_input", required=True, help="path to input image containing ArUCo layout")
ap.add_argument("-p", "--plain", required=True, help="path to input plain image (without markers)")
ap.add_argument("-t", "--input", required=True, help="path to input trial image (with markers)")
ap.add_argument("-o", "--team", required=True, type=str, default="Team", help="Team name")
ap.add_argument("-nt", "--trial", required=True, type=int, default=1, help="Trial numbber")
# number of correct corners
args = vars(ap.parse_args())


if not os.path.exists(args["team"]):
    os.mkdir(args["team"])
team = args["team"]

trial = args["trial"]

if test:
    team_trials_path = "test/"
    output_path="test/scoring/"
    plain_img_path=team_trials_path+args["plain"]
    trial_img_path=team_trials_path+args["input"]
    aruco_img_path=team_trials_path+args["ar_input"]
else:
    team_trials_path = "teams/"+team+"/Perception/"
    output_path="teams/"+team+"/Perception/scoring/"
    plain_img_path=team_trials_path+args["plain"]
    trial_img_path=team_trials_path+args["input"]
    aruco_img_path=team_trials_path+args["ar_input"]


def print_info(activate, arg1, arg2="", arg3="", arg4="", arg5="", arg6=""):
    if(activate):
        print(str(arg1) + str(arg2) + str(arg3) + str(arg4) + str(arg5) + str(arg6))


##### RESIZE IMAGE to fit screen and draw GT #####
def decrease_image(img_path):
    print("\033[94m Reading image: \033[0m", img_path)
    print("\033[94m Resizing image to a ", resize_percent, " % \033[0m")
    img = cv2.imread(img_path) # Load image with aruco layout
    print_info(activate_print, "Original image dim: ", img.shape)
    width = int(img.shape[1] * resize_percent / 100)
    height = int(img.shape[0] * resize_percent / 100)
    dim = (width, height)
    res_img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA) 
    print_info(activate_print, "Resized image to ", resize_percent, "% -> New dim: ", res_img.shape)

    return res_img

def increase_image(img):
    print("\033[94m Restoring image size: \033[0m")
    #print_info(activate_print, "Original image dim: ", img.shape)
    #print("\033[94m Resizing image to a ", resize_percent, " % \033[0m")
    width = int(img.shape[1] / (resize_percent/100))
    height = int(img.shape[0] / (resize_percent/100))
    dim = (width, height)
    res_img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA) 
    print_info(activate_print, "Resized image: ", res_img.shape)

    return res_img


##### GET PX/CM RATIO ####
print("\033[94m GETTING PIXEL/CENTIMETER RATIO \033[0m")
#aruco_img_path=team_trials_path+args["ar_input"]
#px_cm_ratio, px_cm_area_ratio = px_to_cm.transform_perspective(aruco_img_path, resize_percent)
aruco_img = decrease_image(aruco_img_path)
px_cm_ratio, px_cm_area_ratio = px_to_cm.transform_perspective(aruco_img)


##### DEFINE GT #####
# Define ground truth corners and grasping vectors
print("\033[94m DEFINE GROUND TRUTH \033[0m")
#trial_img_path=team_trials_path+args["input"]
#groundtruth_img, corners_coord, vects_end_coord = corner_an.define_groundtruth(trial_img_path, output_path, team, trial, resize_percent, px_cm_ratio)
plain_img = decrease_image(plain_img_path)
trial_img = decrease_image(trial_img_path)
groundtruth_img, trial_gt_img, results, corners_coord, vects_end_coord = corner_an.define_groundtruth(plain_img, trial_img, output_path, team, trial, px_cm_ratio)

print("Corner coordinates: ", corners_coord)
print("Grasping vector end coordinates: ", vects_end_coord)
## Save results
#groundtruth_img = increase_image(groundtruth_img)
#trial_gt_img = increase_image(trial_gt_img)
np.savetxt(output_path+"gt_corners_"+str(trial)+".csv", results, fmt='%s', delimiter=",")   # Save vertices of defined contour
cv2.imwrite(output_path+"gt_"+str(trial)+".png", groundtruth_img)
cv2.imwrite(output_path+"gt_trial_"+str(trial)+".png", trial_gt_img)

# gt_corners_path = output_path+"gt_corners.csv"
# gt_file = csv.reader(open(gt_corners_path))
# gt_data = []
# for rows in gt_file:
#     gt_data.append(rows)
# print(gt_data)
# corner_tolerance_errorpx_cm*2
# cv2.circle(img, (x, y), int(corner_tolerance_error), (255,127,0), 2) # Draw corner detection tolerance #(15,75,50) 
    




# # # Resize image (too small)
# # width = int(groundtruth_img.shape[1] * 300 / 100)
# # height = int(groundtruth_img.shape[0] * 300 / 100)
# # dim = (width, height)
# # img = cv2.resize(groundtruth_img, dim, interpolation = cv2.INTER_AREA)
# # output_img_file=output_path+"trial"+str(trial)+"_results.png"
# # cv2.imwrite(output_img_file, img) # Save with trial number
# # cv2.imshow("Result image", img)
# # cv2.waitKey(0)
# # output_img_file=output_path+"trial"+str(trial)+"_gt.jpg"
# # cv2.imwrite(output_img_file, img) # Save with trial number


## GT image
## Plain image
## trial result
## Eval

# # Compute error corners
# print("\033[94m COMPUTE ERRORS \033[0m")
# plain_img_path=team_trials_path+args["input"] # Plain image path to show results
# results_img, corners_error, scoring = scoring.get_corners_error(plain_img_path, team_trials_path, output_path, team, trial, px_cm_ratio, tolerance, resize_percent)

# # Image to select corners
# print("Show image with results of trial")
# #img = cv2.imread(results_img)
# img = results_img
# # Resize image (too small)
# scale_percent = resize_percent # percent of original size
# width = int(results_img.shape[1] * 300 / 100)
# height = int(results_img.shape[0] * 300 / 100)
# dim = (width, height)
# img = cv2.resize(results_img, dim, interpolation = cv2.INTER_AREA)
# output_img_file=output_path+"trial"+str(trial)+"_results.png"
# cv2.imwrite(output_img_file, img) # Save with trial number
# cv2.imshow("Result image", img)
# cv2.waitKey(0)


# # Measured perimeter and area
# print("\033[94m SAVING TRIAL RESULTS \033[0m")
# results_path = output_path + "trial" +str(trial) + "_results.csv"
# #results_path = team + "/perception/trial" + str(trial) + '_results.csv'
# print("Saving trial ", trial, " results csv in: ", results_path, " as (px/cm ratio, px/cm area ratio, corners coordinates, vector end coordinates, corners error, scoring")
# results_file =open(results_path, 'w')
# writer=csv.writer(results_file)
# row = [px_cm_ratio, px_cm_area_ratio, corners_coord, vects_end_coord, corners_error, scoring]#, vects_error, scoring]
# writer.writerow(row)
# print("Writing results in ", results_path)
# # Info trial (team, trial, config, object, ...), Ratios, perimeter + area (in px and cm), error, points

# #SAVE RESULTS TOTAL
# team_corners_path = team_trials_path+"/trial_grasp_points_" + str(trial) + ".csv"
# gt_corners_path = output_path+"trial"+str(trial)+"_gt.csv"
# print(team_corners_path)
# print(gt_corners_path)
# gt_file = csv.reader(open(gt_corners_path))
# team_file = csv.reader(open(team_corners_path))
# gt_data = []
# team_data = []
# for rows in gt_file:
#     gt_data.append(rows)
# for rows in team_file:
#     team_data.append(rows)

# img = cv2.imread(plain_img_path)
# for i in range(len(gt_data)):
#     print(int(gt_data[i][0]))
#     cv2.line(img, (int(gt_data[i][0]), int(gt_data[i][1])), (int(gt_data[i][2]), int(gt_data[i][3])), (255,127,0), 2)
#     cv2.circle(img, (int(gt_data[i][0]), int(gt_data[i][1])), 3, (255,127,0), -1) #GT color?
# for j in range(len(team_data)):
#     print(int(team_data[j][0]))
#     cv2.line(img, (int(team_data[j][0]), int(team_data[j][1])), (int(team_data[j][2]), int(team_data[j][3])), (0,0,255), 2)
#     cv2.circle(img, (int(team_data[j][0]), int(team_data[j][1])), 3, (0,0,255), -1) #Team color? Red?

# scale_percent = resize_percent # percent of original size
# width = int(img.shape[1] * 300 / 100)
# height = int(img.shape[0] * 300 / 100)
# dim = (width, height)
# img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
# output_img_file=output_path+"trial"+str(trial)+"_results_all.png"
# cv2.imwrite(output_img_file, img) # Save with trial number
# cv2.imshow("Result image", img)
# cv2.waitKey(0)

# #filei.close()

##TODO
# OK Compare corners - Error
# Compare vectors (If corner correct) - Error
# OK Ordenar puntos con sorted (de izq a derecha)
