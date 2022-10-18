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
import scoring


# Get image with Aruco layout
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--ar_input", required=True, help="path to input image containing ArUCo layout")
ap.add_argument("-ii", "--input", required=True, help="path to input image containing result of the trial (folded or flat cloth)")
ap.add_argument("-o", "--output", required=True, type=str, default="Team", help="Team name")
ap.add_argument("-t", "--task", required=True, type=str, default="u", help="Task to score: Task 2.1 Unfolding (u) ot Task 2.2. Folding (f)")
ap.add_argument("-tt", "--trial", required=True, type=int, default=1, help="Trial numbber")
ap.add_argument("-obj", "--object", type=str, default="med_towel", help="Object from the Household Cloth Object Set")
#first or second fold for task folding (o f1, f2)
args = vars(ap.parse_args())


if not os.path.exists(args["output"]):
#    os.mkdir("./ " + args["team"])
    os.mkdir(args["output"])
output_path = args["output"]

trial = args["trial"]

if args["task"] != "u" and args["task"] != "f1" and args["task"] != "f2":
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


# Get px/cm ratio
print("\033[94mGetting pixel/centimeter ratio... \033[0m")
px_cm_ratio, px_cm_area_ratio = px_to_cm.transform_perspective(args["ar_input"])
print("px to cm ratio: ", px_cm_ratio)
print("px to cm AREA ratio: ", px_cm_area_ratio)

# Get cloth perimeter and area in pixels
print("\033[94mDraw the cloth contour\033[0m")
contour_img, cloth_per_px, cloth_area_px = contour_an.draw_contour(args["input"])
print("Measured cloth perimeter (px): ", cloth_per_px)
print("Measured cloth area (px): ", cloth_area_px)

# Compute perimeter and area in cm
print("\033[94mGetting the cloth perimeter and area\033[0m")
cloth_per_cm = cloth_per_px/px_cm_ratio
cloth_area_cm = cloth_area_px/px_cm_area_ratio
print("Measured cloth perimeter (cm): ", cloth_per_cm)
print("Measured cloth area (cm): ", cloth_area_cm)

# Scoring
if args["task"] == "u":
    #call unfolding scoring code
    print("\033[94mScoring Task 2.1. Unfolding!\033[0m")
    size = (50,90)
    scoring.unfolding(CLOTH_SIZE.get(args["object"], None), cloth_per_cm)
elif args["task"] == "f1":
    #call folding scoring code
    print("\033[94mScoring Task 2.2. Folding!\033[0m")
    scoring.folding(CLOTH_SIZE.get(args["object"], None), cloth_per_cm, cloth_area_cm, 2)
elif args["task"] == "f2":
    #call folding scoring code
    print("\033[94mScoring Task 2.2. Folding, second fold!\033[0m")
    scoring.folding(CLOTH_SIZE.get(args["object"], None), cloth_per_cm, cloth_area_cm, 4)
else:
    print("[INFO] Not a manipulation task. Please select unfolding (u) or folding (f). ")
    sys.exit(0)

# Save results
# Contour image
cv2.imwrite(output_path + "trial" + str(trial) + "_cont.jpg", contour_img) # Save with trial number
# Measured perimeter and area
filei =open(output_path + "trial" + str(trial) + '.csv','w')
writer=csv.writer(filei)
row = [px_cm_ratio, px_cm_area_ratio, cloth_per_px, cloth_area_px, cloth_per_cm, cloth_area_cm]
writer.writerow(row)
# Info trial (team, trial, config, object, ...), Ratios, perimeter + area (in px and cm), error, points
#Towel Area: 4500cm2 = 45cm2, Perimeter: 280cm

filei.close()
