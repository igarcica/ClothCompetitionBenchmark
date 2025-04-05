
import cv2
import numpy as np
import sys
sys.path.insert(1, './px_to_cm/')
import new_px_to_cm
import image_interaction

save_imgs = True
trial = 1
corner_tolerance = 2 #Circle radius
appr_vector_tolerance = 45
angle_line_length = 70

## Output directory
# output_path = "./results/"
output_path = "IROS2022/IDLab-AIRO/Perception/scoring/"
input_path =  "IROS2022/IDLab-AIRO/Perception/"

# Load image
image_path = input_path + "calibration.png"
aruco_image = cv2.imread(image_path)

original_image_path = input_path + "trial_input_" +str(trial)+ ".png"
original_image = cv2.imread(original_image_path)

trial_image_path = input_path + "trial_annotated_"+str(trial)+".png" #"test/6_marked.jpg"
trial_image = cv2.imread(trial_image_path)


# # Resize for display (scale to fit screen)
max_display_size = 1000  # Max width or height for display
h, w = aruco_image.shape[:2]
scale_factor = max_display_size / max(h, w)  # Compute the scale factor
# display_image = cv2.resize(aruco_image, (int(w * scale_factor), int(h * scale_factor)))
# cv2.imshow('image', display_image)
# cv2.waitKey(0)



print("\033[94m GETTING PIXEL/CENTIMETER RATIO \033[0m")
px_to_cm = new_px_to_cm.FindHomography(aruco_image, original_image, trial_image, corner_tolerance, appr_vector_tolerance, angle_line_length)
px_to_cm.find_homography()
H = px_to_cm.H
# print("Homography matrix: ", px_to_cm.H)


# Define ground truth corners and grasping vectors
print("\033[94m DEFINE GROUND TRUTH \033[0m")
px_to_cm.set_mode("points_def")
px_to_cm.run()
px_to_cm.set_mode("vector")
px_to_cm.run()
output_img = px_to_cm.trial_image
cv2.imwrite(output_path+"trial_gt_"+str(trial)+".png", output_img)
# corners_groundtruth = image_int.image_interaction()

# px_to_cm.set_mode("distance")
# px_to_cm.run()