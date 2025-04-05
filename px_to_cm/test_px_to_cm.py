import cv2
import numpy as np

# Load image
image_path = "test/pattern.jpg"
original_image = cv2.imread(image_path)

# Resize for display (scale to fit screen)
max_display_size = 1000  # Max width or height for display
h, w = original_image.shape[:2]
scale_factor = max_display_size / max(h, w)  # Compute the scale factor
display_image = cv2.resize(original_image, (int(w * scale_factor), int(h * scale_factor)))
# cv2.imshow('image', display_image)
# cv2.waitKey(0)

# Define ArUco dictionary
ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
ARUCO_PARAMS = cv2.aruco.DetectorParameters_create()

# Detect ArUco markers
corners, ids, _ = cv2.aruco.detectMarkers(original_image, ARUCO_DICT, parameters=ARUCO_PARAMS)

if ids is None or len(ids) < 4:
    print("Error: At least 4 ArUco markers are required.")
    exit()

# Sort markers by ID
ids = ids.flatten()
sorted_indices = np.argsort(ids)  # Sort by marker ID
corners = [corners[i] for i in sorted_indices]
ids = ids[sorted_indices]

# Define real-world spacing (in cm)
real_world_spacing = 7.0  # Adjust based on your actual print

# Set first detected marker as the reference (origin)
origin_id = ids[0]
origin_x, origin_y = 0, 0  # This marker is the new (0,0) in world coordinates

# Store world coordinates dynamically
world_points = []
image_points = []

for i, marker_id in enumerate(ids):
    # Extract the first corner of the marker
    marker_corner = corners[i][0][0]
    print(marker_corner)

    # Calculate relative position based on marker ID
    row = (marker_id-10) // 3  # Assuming a 3x3 grid
    col = (marker_id-10) % 3
    world_x = origin_x + col * real_world_spacing
    world_y = origin_y + row * real_world_spacing

    # Store points
    world_points.append((world_x, world_y)) 
    image_points.append(marker_corner) 

# Convert to NumPy arrays
image_points = np.array(image_points, dtype=np.float32) #Center point of the markers in the real world, considering that the first marker is initialized as (0,0)#Center point of the markers in the real world, considering that the first marker is initialized as (0,0)
world_points = np.array(world_points, dtype=np.float32) #Pixel center points of the markers

# Compute homography
H, _ = cv2.findHomography(image_points, world_points) #This serves to compute image coord into real point

# Function to transform image coordinates to real-world coordinates
def transform_to_real_world(x, y, H):
    img_coords = np.array([[x, y, 1]], dtype=np.float32).T
    real_coords = np.dot(H, img_coords)
    real_coords /= real_coords[2]  # Normalize
    return real_coords[0][0], real_coords[1][0]



######### COMPUTE DISTANCE BETWEEN TWO POINTS
# # Store points clicked
# clicked_points = []

# # Mouse click event to select points
# def select_points(event, x, y, flags, param):
#     global clicked_points
#     if event == cv2.EVENT_LBUTTONDOWN:
#         # Map from display image to original image
#         x_orig, y_orig = int(x / scale_factor), int(y / scale_factor)
#         clicked_points.append((x_orig, y_orig))
#         print(f"Point selected: ({x_orig}, {y_orig})")

#         if len(clicked_points) == 2:
#             # Convert points to real-world coordinates
#             x1, y1 = transform_to_real_world(clicked_points[0][0], clicked_points[0][1], H)
#             x2, y2 = transform_to_real_world(clicked_points[1][0], clicked_points[1][1], H)
#             print(f"Real-world coordinates: ", x1, y1)

#             # Compute Euclidean distance
#             distance_cm = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
#             print(f"Real-world distance: {distance_cm:.2f} cm")

#             # Reset for next selection
#             clicked_points.clear()

# # Display the resized image
# cv2.namedWindow("Select Two Points", cv2.WINDOW_NORMAL)
# cv2.setMouseCallback("Select Two Points", select_points)

# while True:
#     cv2.imshow("Select Two Points", display_image)
#     key = cv2.waitKey(1)
#     if key == 27:  # Press ESC to exit
#         break

# cv2.destroyAllWindows()


############ GRASP POINT

# Function to transform image coordinates to real-world coordinates

# Function to transform real-world coordinates to image coordinates
def transform_to_image_coords(x, y, H_inv):
    real_coords = np.array([[x, y, 1]], dtype=np.float32).T
    img_coords = np.dot(H_inv, real_coords)
    img_coords /= img_coords[2]  # Normalize
    return int(img_coords[0][0]), int(img_coords[1][0])

# Compute inverse homography for mapping back to image space
H_inv = np.linalg.inv(H) #Serves to compute pixel coord from real points

# Store clicked point
clicked_point = []

# Mouse click callback function
def select_center2(event, x, y, flags, param):
    global clicked_point, output_image

    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_point = (x, y)  # Store clicked pixel coordinates
        print(f"Selected pixel: {clicked_point}")

        # Map from display image to original image
        x_orig, y_orig = int(x / scale_factor), int(y / scale_factor)
        print(f"Point selected: ({x_orig}, {y_orig})")
        clicked_point_orig = (x_orig, y_orig)

        # Convert clicked pixel to real-world coordinates
        real_world_center = transform_to_real_world(x_orig, y_orig, H)
        print(f"Real-world coordinates: {real_world_center}")
        print(H)

        # Define a second point 1 cm to the right in real-world coordinates
        real_world_edge = (real_world_center[0] + 1, real_world_center[1])

        # Convert edge point back to image coordinates
        image_edge = transform_to_image_coords(real_world_edge[0], real_world_edge[1], H_inv)

        # Compute pixel radius
        pixel_radius = int(np.linalg.norm(np.array(clicked_point_orig) - np.array(image_edge)))

        # # Map from display image to original image
        # x_displ, y_displ = int(x * scale_factor), int(y * scale_factor)
        # image_point = (x_displ, y_displ)
        pixel_radius_display = int(pixel_radius*scale_factor)

        # Draw the circle
        output_image = display_image.copy()
        cv2.circle(output_image, clicked_point, pixel_radius_display, (0, 255, 0), 2)  # Green circle
        cv2.imshow("Image with Circle", output_image)

# Create a copy of the image for display
output_image = display_image.copy()
# cv2.imshow('image', output_image)

# Display image and set mouse callback
cv2.namedWindow("Select Center", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("Select Center", select_center2)

while True:
    cv2.imshow("Select Center", output_image)
    key = cv2.waitKey(1)
    if key == 27:  # Press ESC to exit
        break

cv2.destroyAllWindows()



########### COMPUTE ANGLE 

# # Store clicked points
# clicked_points = []

# # Function to convert display to original coordinates
# def display_to_original(x, y):
#     orig_x = int(x / scale_factor)
#     orig_y = int(y / scale_factor)
#     return orig_x, orig_y

# # Function to rotate a vector by a given angle
# def rotate_vector(vector, angle_degrees):
#     angle_radians = np.radians(angle_degrees)
#     rotation_matrix = np.array([
#         [np.cos(angle_radians), -np.sin(angle_radians)],
#         [np.sin(angle_radians),  np.cos(angle_radians)]
#     ])
#     return np.dot(rotation_matrix, vector)

# Mouse click callback function
def select_points(event, x, y, flags, param):
    global clicked_points, display_image

    if event == cv2.EVENT_LBUTTONDOWN:
        # Convert display coordinates to original image
        orig_x, orig_y = display_to_original(x, y)
        clicked_points.append((orig_x, orig_y))

        # Draw clicked points
        cv2.circle(display_image, (x, y), 5, (0, 0, 255), -1)  # Red points

        # If two points are clicked, compute the 45º line
        if len(clicked_points) == 2:
            p1, p2 = np.array(clicked_points[0]), np.array(clicked_points[1])
            
            # Compute the direction vector from p1 to p2
            direction = p2 - p1
            direction = direction / np.linalg.norm(direction)  # Normalize

            ## First line angle
            rotated_direction1 = rotate_vector(direction, 45) # Rotate this direction by 45º
            line_length1 = 200  # 100 pixels long # Define line length (adjustable)
            endpoint1 = p1 + rotated_direction1 * line_length1 # Compute the endpoint

            ## Second line angle
            rotated_direction2 = rotate_vector(direction, -45) # Rotate this direction by 45º
            line_length2 = 200  # pixels long # Define line length (adjustable)
            endpoint2 = p1 + rotated_direction2 * line_length2 # Compute the endpoint

            # Convert back to display coordinates
            disp_p1 = (int(p1[0] * scale_factor), int(p1[1] * scale_factor))
            disp_endpoint1 = (int(endpoint1[0] * scale_factor), int(endpoint1[1] * scale_factor))
            disp_endpoint2 = (int(endpoint2[0] * scale_factor), int(endpoint2[1] * scale_factor))

            # Draw the original reference line (p1 -> p2)
            disp_p2 = (int(p2[0] * scale_factor), int(p2[1] * scale_factor))
            cv2.line(display_image, disp_p1, disp_p2, (255, 0, 0), 2)  # Blue reference line

            # Draw the rotated line (45º from p1)
            cv2.line(display_image, disp_p1, disp_endpoint1, (0, 0, 0), 2)  # Green rotated line
            cv2.line(display_image, disp_p1, disp_endpoint2, (0, 0, 0), 2)  # Green rotated line

            # Create shadow effect using a filled triangle
            # Create a semi-transparent shadow overlay
            overlay = display_image.copy()
            triangle_pts = np.array([disp_p1, disp_endpoint1, disp_endpoint2], np.int32)
            cv2.fillPoly(overlay, [triangle_pts], (50, 50, 50))  # Dark gray
            # display_image_copy = display_image.copy()
            # triangle_pts = np.array([disp_p1, disp_endpoint1, disp_endpoint2], np.int32)
            # cv2.fillPoly(display_image, [triangle_pts], (50, 50, 50, 100))  # Dark gray shadow
            # image_new = cv2.addWeighted(display_image, 0.5, display_image_copy, 1 - 0.5, 0) #opacity of triangle
            alpha = 0.4 # Triangle opacity
            display_image = cv2.addWeighted(overlay, alpha, display_image, 1 - alpha, 0)

            # Show updated image
            # cv2.imshow("Select Points", image_new)

# Create display window
cv2.namedWindow("Select Points", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("Select Points", select_points)

while True:
    cv2.imshow("Select Points", display_image)
    key = cv2.waitKey(1)
    if key == 27:  # Press ESC to exit
        break

cv2.destroyAllWindows()
