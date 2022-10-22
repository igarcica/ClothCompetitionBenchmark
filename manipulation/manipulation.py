# Draw contour
# Measure area in cm
# Compute unfolding error --> Given the object name and a dictionary
# Based on threshold, compute points

import csv
import cv2
import argparse
import os
import sys
sys.path.insert(1, './px_cm/')
import px_to_cm
import contour_annotation as contour_an
import manipulation_scoring as scoring

resize_percent = 300 

# Get image with Aruco layout
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--ar_input", required=True, help="path to input image containing ArUCo layout")
ap.add_argument("-ii", "--input", required=True, help="path to input image containing result of the trial (folded or flat cloth)")
ap.add_argument("-o", "--team", required=True, type=str, default="Team", help="Team name")
ap.add_argument("-t", "--task", required=True, type=str, default="u", help="Task to score: Task 2.1 Unfolding (u) ot Task 2.2. Folding (f)")
ap.add_argument("-tt", "--trial", required=True, type=int, default=1, help="Trial numbber")
ap.add_argument("-obj", "--object", type=str, default="med_towel", help="Object from the Household Cloth Object Set")
#first or second fold for task folding (o f1, f2)
args = vars(ap.parse_args())


if not os.path.exists(args["team"]):
#    os.mkdir("./ " + args["team"])
    os.mkdir(args["team"])
team = args["team"]

trial = args["trial"]

if args["task"] != "u" and args["task"] != "f" and args["task"] != "f1" and args["task"] != "f2":
    print("[INFO] Not a manipulation task. Please select unfolding (u) or folding (f). ")
    sys.exit(0)

#Household Cloth Object Set dictionary
CLOTH_SIZE = {
        "small_towel": (30,50),
        "med_towel": (50,90),
        "big_towel":(90, 150),
        "bedhseet": (160, 280),
        "fit_bedsheet": (90, 200),
        "sq_pillowcase": (60, 60),
        "rect_pillowcase": (45, 110),
        "rect_tablecloth": (170, 250),
        "round_tablecloth": 200,
        "cotton_napkin": (50, 50),
        "linen_napkin": (50, 50),
        "towel_rag": (50, 70),
        "linen_rag": (50, 70),
        "waffle_rag": (50, 70),
        "chekered_rag": (50, 70)
        }

if CLOTH_SIZE.get(args["object"], None) is None:
        print("[INFO] Object '{}' is not from the Household Cloth Object Set".format(args["object"]))
        sys.exit(0)


team_trials_path = "teams_trials/"+team+"/Folding/"
output_path="teams_trials/"+team+"/Folding/scoring/"


# Get px/cm ratio
print("\033[94m GETTING PIXEL/CENTIMETER RATIO \033[0m")
aruco_img_path=team_trials_path+args["ar_input"]
px_cm_ratio, px_cm_area_ratio = px_to_cm.transform_perspective(aruco_img_path, resize_percent)


# Get starting configuration cloth perimeter and area in pixels
print("\033[94m DEFINE INITIAL CONFIG CONTOUR \033[0m")
trial_img_path=team_trials_path+"trial_start_"+str(trial)+".png"
init_contour_img, init_cloth_per_px, init_cloth_area_px = contour_an.draw_contour(trial_img_path, resize_percent)
print("INIT Measured cloth perimeter (px): ", init_cloth_per_px)
print("INIT Measured cloth area (px): ", init_cloth_area_px)

# Get cloth perimeter and area in pixels
print("\033[94m DEFINE CONTOUR FIRST FOLD \033[0m")
trial_img_path=team_trials_path+args["input"]
f1_contour_img, f1_cloth_per_px, f1_cloth_area_px = contour_an.draw_contour(trial_img_path, resize_percent)
print("FIRST measured cloth perimeter (px): ", f1_cloth_per_px)
print("FIRST measured cloth area (px): ", f1_cloth_area_px)

# Compute perimeter and area in cm
print("\033[94mGetting the cloth perimeter and area\033[0m")
f1_cloth_per_cm = f1_cloth_per_px/px_cm_ratio
f1_cloth_area_cm = f1_cloth_area_px/px_cm_area_ratio
print("FIRST FOLD Measured cloth perimeter (cm): ", f1_cloth_per_cm)
print("FIRST FOLD Measured cloth area (cm): ", f1_cloth_area_cm)

# Get cloth perimeter and area in pixels
print("\033[94m DEFINE CONTOUR SECOND FOLD \033[0m")
trial_img_path=team_trials_path+"trial_final_"+str(trial)+".png"
f2_contour_img, f2_cloth_per_px, f2_cloth_area_px = contour_an.draw_contour(trial_img_path, resize_percent)
print("SECOND FOLD  Measured cloth perimeter (px): ", f2_cloth_per_px)
print("SECOND FOLD Measured cloth area (px): ", f2_cloth_area_px)

# Compute perimeter and area in cm
print("\033[94mGetting the cloth perimeter and area\033[0m")
f2_cloth_per_cm = f2_cloth_per_px/px_cm_ratio
f2_cloth_area_cm = f2_cloth_area_px/px_cm_area_ratio
print("SECOND FOLD Measured cloth perimeter (cm): ", f2_cloth_per_cm)
print("SECOND FOLD Measured cloth area (cm): ", f2_cloth_area_cm)

# Scoring
if args["task"] == "u":
    #call unfolding scoring code
    print("\033[94mScoring Task 2.1. Unfolding!\033[0m")
    size = (50,90)
    scoring.unfolding(CLOTH_SIZE.get(args["object"], None), cloth_per_cm)
elif args["task"] == "f":
    #call folding scoring code
    print("\033[94mScoring Task 2.2. Folding!\033[0m")
    obj_real_perimeter, obj_real_area, error_perimeter_f1, error_area_f1 = scoring.folding(CLOTH_SIZE.get(args["object"], None), init_cloth_area_px, f1_cloth_per_px, f1_cloth_per_cm, f1_cloth_area_px, f1_cloth_area_cm)
    print("\033[92m First fold perimeter error ", f1_cloth_area_px/(init_cloth_area_px)/2, "\033[0m")
    print(f1_cloth_area_px, " / ", (init_cloth_area_px)/2, " / ", f1_cloth_area_px/init_cloth_area_px/2)
    obj_real_perimeter_f2, obj_real_area_f2, error_perimeter_f2, error_area_f2 = scoring.folding2(CLOTH_SIZE.get(args["object"], None), init_cloth_area_px, f2_cloth_per_px, f2_cloth_per_cm, f2_cloth_area_px, f2_cloth_area_cm)
    print("\033[92m Seccond fold perimeter error ", f2_cloth_area_px/(init_cloth_area_px/4), "\033[0m")
else:
    print("[INFO] Not a manipulation task. Please select unfolding (u) or folding (f). ")
    sys.exit(0)

## Save results
## Contour image
#cv2.imwrite(output_path + "/trial" + str(trial) + "_cont.jpg", contour_img) # Save with trial number
## Measured perimeter and area
#filei =open(output_path + "/trial" + str(trial) + '.csv','w')
#writer=csv.writer(filei)
#row = [px_cm_ratio, px_cm_area_ratio, cloth_per_px, cloth_area_px, cloth_per_cm, cloth_area_cm]
#writer.writerow(row)
## Info trial (team, trial, config, object, ...), Ratios, perimeter + area (in px and cm), error, points
##Towel Area: 4500cm2 = 45cm2, Perimeter: 280cm
#
#filei.close()

##TODO
#Compare area with initial!
