# Draw contour
# Measure area in cm
# Compute unfolding error --> Given the object name and a dictionary
# Based on threshold, compute points

import argparse
import cv2
import sys
sys.path.insert(1, './px_cm/')
import px_to_cm
import contour_annotation as contour_an


# Get image with Aruco layout
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--ar_input", required=True, help="path to input image containing ArUCo layout")
ap.add_argument("-ii", "--input", required=True, help="path to input image containing result of the trial (folded or flat cloth)")
ap.add_argument("-t", "--task", required=True, type=str, default="u", help="Task to score: Task 2.1 Unfolding (u) ot Task 2.2. Folding (f)")
args = vars(ap.parse_args())

if args["task"] != "u" and args["task"] != "f":
    print("[INFO] Not a manipulation task. Please select unfolding (u) or folding (f). ")
    sys.exit(0)

# Get px/cm ratio
print("Getting pixel/centimeter ratio...")
px_cm_ratio, px_cm_area_ratio = px_to_cm.transform_perspective(args["ar_input"])
print("px to cm ratio: ", px_cm_ratio)
print("px to cm AREA ratio: ", px_cm_area_ratio)

# Get cloth perimeter and area in pixels
print("Draw the cloth contour")
cloth_per_px, cloth_area_px = contour_an.draw_contour(args["input"])
print("Cloth perimeter (px): ", cloth_per_px)
print("Cloth area (px): ", cloth_area_px)

# Compute perimeter and area in cm
print("Getting the cloth perimeter and area")
cloth_per_cm = cloth_per_px/px_cm_ratio
cloth_area_cm = cloth_area_px/px_cm_area_ratio
print("Cloth perimeter (cm): ", cloth_per_cm)
print("Cloth area (cm): ", cloth_area_cm)

# Scoring
if args["task"] == "u":
    #call unfolding scoring code
    print("Scoring Task 2.1. Unfolding!")
elif args["task"] == "f":
    #call folding scoring code
    print("Scoring Task 2.2. Folding!")
else:
    print("[INFO] Not a manipulation task. Please select unfolding (u) or folding (f). ")
    sys.exit(0)
