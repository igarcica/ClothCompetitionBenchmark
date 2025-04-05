
import cv2
import numpy as np

class ImageInteraction:
    def __init__(self, original_image, H, save_imgs=False):
        """
        Initialize with:
        - 
        """
        self.original_image, = original_image,
        # self.scale_factor = scale_factor
        self.H = H

        # Resize for display (scale to fit screen)
        max_display_size = 1000  # Max width or height for display
        h, w = original_image.shape[:2]
        self.scale_factor = max_display_size / max(h, w)  # Compute the scale factor
        self.display_image = cv2.resize(self.original_image, (int(w * self.scale_factor), int(h * self.scale_factor)))
    
    def set_mode(self,  mode):
        """Set the mode of interaction (distance, points_def, vector)."""
        self.mode = mode
        self.clicked_points = []  # Reset clicked points when mode changes
        print(f"Mode set to: {self.mode}")

    def display_to_original(self, x, y):
        """Convert display coordinates to original image coordinates."""
        # Map from display image to original image
        x_orig, y_orig = int(x / self.scale_factor), int(y / self.scale_factor)
        print(f"Point selected: ({x_orig}, {y_orig})")
        return x_orig, y_orig

    def image_interaction(self, event, x, y, flags, param):
        """Mouse callback function to handle different actions based on the mode."""
        if event == cv2.EVENT_LBUTTONDOWN:
            orig_x, orig_y = self.display_to_original(x, y)
            self.clicked_points.append((orig_x, orig_y))

            if self.mode == "distance":
                if len(self.clicked_points) == 2:
                    ## Distance in pixels
                    p1, p2 = np.array(self.clicked_points[0]), np.array(self.clicked_points[1])
                    distance_px = np.linalg.norm(p2 - p1)
                    print(f"Distance (pixels): {distance_px:.2f}")

                    # Convert to display coordinates and draw line
                    disp_p1 = (int(p1[0] * self.scale_factor), int(p1[1] * self.scale_factor))
                    disp_p2 = (int(p2[0] * self.scale_factor), int(p2[1] * self.scale_factor))
                    cv2.line(self.display_image, disp_p1, disp_p2, (255, 255, 0), 2)  # Yellow line

                    ## Distance in centimeters - Convert points to real-world coordinates
                    x1, y1 = transform_to_real_world(clicked_points[0][0], clicked_points[0][1], H) 
                    x2, y2 = transform_to_real_world(clicked_points[1][0], clicked_points[1][1], H)
                    print(f"Real-world coordinates: ", x1, y1)

                    # Compute Euclidean distance
                    distance_cm = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                    print(f"Real-world distance: {distance_cm:.2f} cm")

                    # Reset for next selection
                    clicked_points.clear()

            elif self.mode == "points_def":
                if len(self.clicked_points) == 1:
                    radius_px = int(2 / self.scale_factor)  # Assuming 2cm converted to pixels
                    disp_center = (int(orig_x * self.scale_factor), int(orig_y * self.scale_factor))
                    cv2.circle(self.display_image, disp_center, radius_px, (0, 255, 255), 2)  # Cyan circle

            elif self.mode == "vector":
                if len(self.clicked_points) == 2:
                    p1, p2 = np.array(self.clicked_points[0]), np.array(self.clicked_points[1])
                    direction = p2 - p1
                    direction = direction / np.linalg.norm(direction)  # Normalize
                    rotated_direction = self.rotate_vector(direction, 45)
                    endpoint = p1 + rotated_direction * self.line_length

                    # Convert to display coordinates
                    disp_p1 = (int(p1[0] * self.scale_factor), int(p1[1] * self.scale_factor))
                    disp_p2 = (int(p2[0] * self.scale_factor), int(p2[1] * self.scale_factor))
                    disp_endpoint = (int(endpoint[0] * self.scale_factor), int(endpoint[1] * self.scale_factor))

                    # Draw original reference line (p1 -> p2)
                    cv2.line(self.display_image, disp_p1, disp_p2, (255, 0, 0), 2)  # Blue reference line

                    # Draw rotated line (45º from p1)
                    cv2.line(self.display_image, disp_p1, disp_endpoint, (0, 255, 0), 2)  # Green rotated line

                    # Create semi-transparent shadow
                    overlay = self.display_image.copy()
                    triangle_pts = np.array([disp_p1, disp_p2, disp_endpoint], np.int32)
                    cv2.fillPoly(overlay, [triangle_pts], (50, 50, 50))  # Dark gray shadow
                    self.display_image = cv2.addWeighted(overlay, self.opacity, self.display_image, 1 - self.opacity, 0)

            # Show updated image
            cv2.imshow("Interactive Drawing", self.display_image)
            

    def run(self):
        """Main function to run the interactive window."""
        cv2.namedWindow("Interactive Drawing", cv2.WINDOW_NORMAL)
        cv2.setMouseCallback("Interactive Drawing", self.image_interaction)

        print("Press '1' for Distance Mode, '2' for Circle Mode, '3' for Angle Mode.")
        
        while True:
            cv2.imshow("Interactive Drawing", self.display_image)
            key = cv2.waitKey(1)
            
            if key == 27:  # ESC to exit
                break
            # elif key == ord('1'):
            #     self.set_mode("distance")
            # elif key == ord('2'):
            #     self.set_mode("circle")
            # elif key == ord('3'):
            #     self.set_mode("angle")

        cv2.destroyAllWindows()


# ######### COMPUTE DISTANCE BETWEEN TWO POINTS
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