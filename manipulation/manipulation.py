import cv2
import numpy as np
import sys
sys.path.insert(1, './px_to_cm/')
import new_px_to_cm

save_imgs = True
trial = 2
corner_tolerance = 2 #Circle radius
appr_vector_tolerance = 45
angle_line_length = 70
max_display_size = 1500  # Max width or height for display
object_name = "linen_napkin" 
task = "folding2" 

## Output directory
# output_path = "./results/"
output_path = "IROS2022/Shinshu/Unfolding/scoring/"
input_path =  "IROS2022/Shinshu/Unfolding/"

# Load image
image_path = input_path + "UR5e_system_aruco_image.png"
aruco_image = cv2.imread(image_path)

original_image_path = input_path + "image_0.png" #"trial_start_1.png" #str(trial)+ "_pre-fold.jpg"
original_image = cv2.imread(original_image_path)

trial_image_path = input_path +str(trial)+ "_pre-fold.jpg"
trial_image = cv2.imread(trial_image_path)


# # Resize for display (scale to fit screen)
h, w = aruco_image.shape[:2]
scale_factor = max_display_size / max(h, w)  # Compute the scale factor

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
        "checkered_rag": (50, 70),
        "paper": (21, 29.7)
        }

# object_dims = CLOTH_SIZE.get(args["object"], None)
object_dims = CLOTH_SIZE.get(object_name, None)
print("Object flat dimensions", object_dims)

def rescale_image(image, max_display_size):
    # Resize for display (scale to fit screen)
    h, w = image.shape[:2]
    scale_factor = max_display_size / max(h, w)  # Compute the scale factor
    rescaled_image = cv2.resize(image, (int(w * scale_factor), int(h * scale_factor)))
    # self.display_image = original_image.copy()
    return scale_factor, rescaled_image

def unfolding_coverage(real_obj_size, measured_area_cm):
    real_perimeter_cm = (real_obj_size[0]+real_obj_size[1])*2
    real_area_cm = real_obj_size[0]*real_obj_size[1]
    print("Real cloth perimeter (cm): ", real_perimeter_cm)
    print("Real cloth area (cm): ", real_area_cm)

    coverage = measured_area_cm / real_area_cm
    coverage = (max(0, min(coverage, 1)))*100 #If measured area is > than real area then 100% coverage
    print("Coverage (%): ", coverage)
    area_error = (1-coverage) # Percetange of area error

    return coverage, area_error #, real_perimeter_cm, real_area_cm


# def first_fold_coverage(real_obj_size, measured_area_cm):
def fold_iot_error(real_perimeter_cm, real_area_cm, measured_area_cm):
    # real_perimeter_cm = (real_obj_size[0]+real_obj_size[1]/2)*2 #Half of the total area
    # real_area_cm = (real_obj_size[0]*real_obj_size[1])/2
    print("Real folded cloth perimeter (cm): ", real_perimeter_cm, " cm")
    print("Real folded cloth area (cm): ", real_area_cm, " cm")

    # # ERROR with REAL OBJECT SIZE - AREA
    # coverage = measured_area_cm/real_area_cm
    # coverage = (max(0, min(coverage, 1)))*100
    # area_error = 100-coverage
    # print("Coverage (%): ", coverage)
    # print("\033[33m First fold error: ", area_error, "% \033[0m")

    fold_error = abs((measured_area_cm/real_area_cm)-1)*100
    print("Folding error: ", fold_error)

    return fold_error


    real_perimeter_cm = (real_obj_size[0]+real_obj_size[1]) # 1/4 of flat area
    real_area_cm = (real_obj_size[0]*real_obj_size[1])/4
    print("Real folded cloth perimeter (cm): ", real_perimeter_cm, " cm")
    print("Real folded cloth area (cm): ", real_area_cm, " cm")

    # ERROR with REAL OBJECT SIZE - AREA
    coverage = measured_area_cm/real_area_cm
    coverage = (max(0, min(coverage, 1)))*100
    area_error = 100-coverage
    print("Coverage (%): ", coverage)
    print("\033[33m First fold error: ", area_error, "% \033[0m")

    return coverage, area_error

##### SAVE RESULTS #####
def save_results(contour_vert, img, results_data):
    print("\033[94m Saving results \033[0m")

    # Save measured results
    np.savetxt(output_path+str(trial)+"_results_data"+".csv", results_data, fmt='%s', delimiter=",")

    # Save vertices of defined contour
    np.savetxt(output_path+str(trial)+"_vertices.csv", contour_vert, fmt='%s', delimiter=",")   

    # # Save image with defined contour
    # error = results_data[2][1]
    # text_loc = img.shape
    # text = "Error: " + str(round(abs(error),2)) +"%"
    # cv2.putText(img, text, (int((text_loc[1]/2)-100), int(text_loc[0]/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
    


########################################
# print("\033[94m GETTING PIXEL/CENTIMETER RATIO \033[0m")
scale_factor, original_image_scaled = rescale_image(original_image, max_display_size)
px_to_cm = new_px_to_cm.FindHomography(aruco_image, original_image_scaled, original_image_scaled, scale_factor)
px_to_cm.find_homography()
# H = px_to_cm.H
# print(H)
## Check calibration
# px_to_cm.set_mode("distance")
# px_to_cm.run("Draw contour")

## If the arucos are nos detected, homography can be computed by clicking and saving the aruco pixel points
# # image_points = [[1153.,  596.], [1092.,  596.], [1031.,  597.], [1153.,  535.], [1092.,  535.], [1031.,  535.], [1154.,  473.], [1092.,  473.], [1030.,  474.]] #First corner of the markers (in order of ID)
# image_points = [[150.,  135.], [134.,  135.], [118.,  133.], [152.,  119.], [136.,  118.], [118., 117.], [152.,  103.], [136., 102.], [120., 101.]] ##IDLab-AIRO IROS2022
# world_points = [(0.0, 0.0), (7.0, 0.0), (14.0, 0.0), (0.0, 7.0), (7.0, 7.0), (14.0, 7.0), (0.0, 14.0), (7.0, 14.0), (14.0, 14.0)]
# px_to_cm.manual_homography(world_points, image_points)
# print(px_to_cm.H)
# px_to_cm.set_mode("distance")
# px_to_cm.run("Draw contour")

if task == "unfolding":
    ## Draw contour to compute coverage
    print("\033[94m DEFINE CONTOUR \033[0m")
    px_to_cm.set_mode("draw_contour")
    px_to_cm.run("Draw contour")
    u_vertices = px_to_cm.clicked_points
    area_cm = px_to_cm.area_cm
    print("Area (cm): ", area_cm)

    real_perimeter_cm = (object_dims[0]+object_dims[1])*2
    real_area_cm = object_dims[0]*object_dims[1]

    u_coverage, u_percentage_area_error = unfolding_coverage(object_dims, area_cm)
    #Save image
    u_contour_img = px_to_cm.display_image
    cv2.imwrite(output_path+"trial_gt_"+str(trial)+".png", u_contour_img)
    # Save results
    u_results = [["Real perimeter (cm)", real_perimeter_cm], ["Real area (cm)", real_area_cm], ["Measured perimeter (cm)", px_to_cm.perimeter_cm], ["Measured area (cm)", px_to_cm.area_cm], ["Coverage (%)", u_coverage], ["Area error (%)", u_percentage_area_error]] 
    save_results(u_vertices, u_contour_img, u_results)

elif task == "folding1": #First fold
    ## Draw contour to compute coverage
    print("\033[94m DEFINE CONTOUR \033[0m")
    px_to_cm.set_mode("draw_contour")
    px_to_cm.run("Draw contour")
    f1_vertices = px_to_cm.clicked_points
    measured_area_cm = px_to_cm.area_cm
    print("Area (cm): ", measured_area_cm)

    real_perimeter_cm = (object_dims[0]+object_dims[1]/2)*2 #Half of the total area
    real_area_cm = (object_dims[0]*object_dims[1])/2
    f1_percentage_fold_error = fold_iot_error(real_perimeter_cm, real_area_cm, measured_area_cm)

    #Save image
    f1_contour_img = px_to_cm.display_image
    cv2.imwrite(output_path+str(trial)+"_f1_trial_gt.png", f1_contour_img)
    # Save results
    f1_results = [["Real perimeter (cm)", real_perimeter_cm], ["Real area (cm)", real_area_cm], ["Measured perimeter (cm)", px_to_cm.perimeter_cm], ["Measured area (cm)", px_to_cm.area_cm], ["Fold error (%)", f1_percentage_fold_error]] 
    save_results(f1_vertices, f1_contour_img, f1_results)


elif task == "folding2":
    ## Draw contour to compute coverage
    print("\033[94m DEFINE CONTOUR \033[0m")
    px_to_cm.set_mode("draw_contour")
    px_to_cm.run("Draw contour")
    f2_vertices = px_to_cm.clicked_points
    measured_area_cm = px_to_cm.area_cm
    print("Area (cm): ", measured_area_cm)

    real_perimeter_cm = (object_dims[0]+object_dims[1]) # 1/4 of flat area
    real_area_cm = (object_dims[0]*object_dims[1])/4
    f2_percentage_fold_error = fold_iot_error(real_perimeter_cm, real_area_cm, measured_area_cm)

    #Save image
    f2_contour_img = px_to_cm.display_image
    cv2.imwrite(output_path+str(trial)+"_f2_trial_gt.png", f2_contour_img)
    # Save results
    f2_results = [["Real perimeter (cm)", real_perimeter_cm], ["Real area (cm)", real_area_cm], ["Measured perimeter (cm)", px_to_cm.perimeter_cm], ["Measured area (cm)", px_to_cm.area_cm], ["Fold error (%)", f2_percentage_fold_error]] 
    save_results(f2_vertices, f2_contour_img, f2_results)

