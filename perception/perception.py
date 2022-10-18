
import argparse
import os
import sys
sys.path.insert(1, './px_cm/')
import px_to_cm
import corner_annotation as corner_an

# Get image with Aruco layout
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--ar_input", required=True, help="path to input image containing ArUCo layout")
ap.add_argument("-ii", "--input", required=True, help="path to input image containing result of the trial (cloth with perceived corners and vectors)")
ap.add_argument("-o", "--team", required=True, type=str, default="Team", help="Team name")
ap.add_argument("-tt", "--trial", required=True, type=int, default=1, help="Trial numbber")
# number of correct corners
args = vars(ap.parse_args())


if not os.path.exists(args["team"]):
    os.mkdir(args["team"])
output_path = args["team"]

trial = args["trial"]


# Get px/cm ratio
print("\033[94mGetting pixel/centimeter ratio... \033[0m")
px_cm_ratio, px_cm_area_ratio = px_to_cm.transform_perspective(args["ar_input"])
print("px to cm ratio: ", px_cm_ratio)
print("px to cm AREA ratio: ", px_cm_area_ratio)

# Define ground truth corners and grasping vectors
groundtruth_img, corner_coord, vect_end_coord = corner_an.define_groundtruth(args["input"])
print("Corner coordinates: ", corner_coord)
print("Grasping vector end coordinates: ", vect_end_coord)

# Compare corners - Error
# Compare vectors (If corner correct) - Error



## Save results
## Groundtruth image
#cv2.imwrite(output_path + "trial" + str(trial) + "_cont.jpg", contour_img) # Save with trial number
## Measured perimeter and area
#filei =open(output_path + "trial" + str(trial) + '.csv','w')
#writer=csv.writer(filei)
#row = [px_cm_ratio, px_cm_area_ratio, corner_coord, vect_end_coord, corner_error, vect_error, scoring]
#writer.writerow(row)
## Info trial (team, trial, config, object, ...), Ratios, perimeter + area (in px and cm), error, points

#filei.close()
