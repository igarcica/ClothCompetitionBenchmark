
import cv2
import numpy as np
import sys
sys.path.insert(1, './px_to_cm/')
import new_px_to_cm


save_imgs = True
trial = 5
corner_tolerance = 2 #Circle radius
appr_vector_tolerance = 45
angle_line_length = 70


#### TEAM SETTINGS

# ## ---UMich IROS 2022:
# output_path = "IROS2022/UMich/Perception/scoring/"
# input_path =  "IROS2022/UMich/Perception/"
# image_path = input_path + "tag_image_0_marked.png" # Aruco marker image
# original_image_path = input_path + "results_image_" + str(trial) + ".png"  # Trial plain image without markers
# trial_image_path = input_path + "results_image_" + str(trial) + "_marked.png" #Trial image with markers
# max_display_size = 1500  # Max width or height for display

# ## ---IDLab-AIRO 2023:
# output_path = "ICRA2023/IDLab-AIRO/Perception/scoring/"
# input_path =  "ICRA2023/IDLab-AIRO/Perception/"
# image_path = input_path + "competition_marker.png" # Aruco marker image
# original_image_path = input_path + "000" + str(trial) + "_image_original.png"  # Trial plain image without markers
# trial_image_path = input_path + "000" + str(trial) + "_image_competition.png" #Trial image with markers
# max_display_size = 1500  # Max width or height for display

# ## ---ViCoS-FRI 2023:
# output_path = "ICRA2023/ViCoS-FRI/Perception/scoring/"
# input_path =  "ICRA2023/ViCoS-FRI/Perception/"
# image_path = input_path + "0_input.jpg" # Aruco marker image
# original_image_path = input_path + str(trial) + "_input.jpg"  # Trial plain image without markers
# trial_image_path = input_path + str(trial) + "_marked.jpg" #Trial image with markers
# max_display_size = 1500  # Max width or height for display

## ---Shinshu
output_path = "IROS2022/Shinshu/Perception/scoring/"
input_path =  "IROS2022/Shinshu/Perception/"
image_path = input_path + "UR5e_system_aruco_image.png"
original_image_path = input_path + "trial_" + str(trial) + ".png" # Trial plain image without markers
trial_image_path = input_path + "trial_" + str(trial) + "_marked.png" #Trial image with markers
max_display_size = 1500  # Max width or height for display


# Load images
aruco_image = cv2.imread(image_path)
original_image = cv2.imread(original_image_path)
trial_image = cv2.imread(trial_image_path)

# # # Resize for display (scale to fit screen)
# # max_display_size = 1000  # Max width or height for display
# h, w = aruco_image.shape[:2]
# scale_factor = max_display_size / max(h, w)  # Compute the scale factor
# # display_image = cv2.resize(aruco_image, (int(w * scale_factor), int(h * scale_factor)))
# # cv2.imshow('image', display_image)
# # cv2.waitKey(0)

def rescale_image(image, max_display_size):
    # Resize for display (scale to fit screen)
    h, w = image.shape[:2]
    scale_factor = max_display_size / max(h, w)  # Compute the scale factor
    rescaled_image = cv2.resize(image, (int(w * scale_factor), int(h * scale_factor)))
    # self.display_image = original_image.copy()
    return scale_factor, rescaled_image


print("\033[94m GETTING PIXEL/CENTIMETER RATIO \033[0m")
scale_factor, original_image_scaled = rescale_image(original_image, max_display_size)
scale_factor, trial_image_scaled = rescale_image(trial_image, max_display_size)
px_to_cm = new_px_to_cm.FindHomography(aruco_image, original_image_scaled, trial_image_scaled, scale_factor, corner_tolerance, appr_vector_tolerance, angle_line_length)
# px_to_cm = new_px_to_cm.FindHomography(aruco_image, original_image_scaled, original_image_scaled, scale_factor)
px_to_cm.find_homography()
H = px_to_cm.H
# print("Homography matrix: ", px_to_cm.H)


# Define ground truth corners and grasping vectors
print("\033[94m DEFINE GROUND TRUTH \033[0m")
# px_to_cm.set_mode("points_def")
# px_to_cm.run("Draw GT")
px_to_cm.set_mode("corner_gt")
px_to_cm.run("Draw GT")
output_img = px_to_cm.trial_image
cv2.imwrite(output_path+"trial_gt_"+str(trial)+".png", output_img)
# corners_groundtruth = image_int.image_interaction()

# px_to_cm.set_mode("distance")
# px_to_cm.run()





