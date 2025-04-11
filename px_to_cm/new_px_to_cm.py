import cv2
import numpy as np



class FindHomography:
    def __init__(self, aruco_image, original_image, trial_image, scale_factor, circle_radius=1, vector_tolerance=45, angle_lines_length=200):
        """
        Initialize with:
        - 
        """
        self.aruco_image = aruco_image # To get homography
        self.original_image = original_image # To draw the groundtruth
        self.trial_image = trial_image  # To save the groundtruth in the trial image
        self.display_image = original_image #To see the image

        self.scale_factor = scale_factor
        self.H = 0
        self.clicked_points = []


        # # self.scale_factor = scale_factor
        # # Resize for display (scale to fit screen)
        # max_display_size = 1500  # Max width or height for display
        # h, w = original_image.shape[:2]
        # self.scale_factor = max_display_size / max(h, w)  # Compute the scale factor
        # self.display_image = cv2.resize(self.original_image, (int(w * self.scale_factor), int(h * self.scale_factor)))
        # # self.display_image = original_image.copy()
    
        # self.aruco_image = cv2.resize(self.aruco_image, (int(w * self.scale_factor), int(h * self.scale_factor)))
        # cv2.imshow("Image with Circle", self.aruco_image)

        # # Resize trial image
        # self.trial_image = cv2.resize(self.trial_image, (int(w * self.scale_factor), int(h * self.scale_factor)))

        self.circle_radius = circle_radius
        self.vector_tol = vector_tolerance
        self.angle_lines_length = angle_lines_length
        self.area_cm = 0
        self.perimeter_cm = 0

    def find_homography(self):

        # Define ArUco dictionary
        ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        ARUCO_PARAMS = cv2.aruco.DetectorParameters_create()

        # Detect ArUco markers
        corners, ids, _ = cv2.aruco.detectMarkers(self.aruco_image, ARUCO_DICT, parameters=ARUCO_PARAMS)

        if ids is None or len(ids) < 9:
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

            # Calculate relative position based on marker ID
            row = (marker_id-10) // 3  # Assuming a 3x3 grid
            col = (marker_id-10) % 3
            world_x = origin_x + col * real_world_spacing
            world_y = origin_y + row * real_world_spacing

            # Store points
            world_points.append((world_x, world_y)) 
            image_points.append(marker_corner) 

        print(world_points)
        print(image_points)
        
        # Convert to NumPy arrays
        image_points = np.array(image_points, dtype=np.float32) #Center point of the markers in the real world, considering that the first marker is initialized as (0,0)#Center point of the markers in the real world, considering that the first marker is initialized as (0,0)
        world_points = np.array(world_points, dtype=np.float32) #Pixel center points of the markers

        print(world_points)
        print(image_points)
        
        # Compute homography (Perspective Transformation)
        self.H, _ = cv2.findHomography(image_points, world_points) #This serves to compute image coord into real point
    
    def manual_homography(self, world_points, image_points):

        print(world_points)
        print(image_points)

        # Convert to NumPy arrays
        image_points = np.array(image_points, dtype=np.float32) #Center point of the markers in the real world, considering that the first marker is initialized as (0,0)#Center point of the markers in the real world, considering that the first marker is initialized as (0,0)
        world_points = np.array(world_points, dtype=np.float32) #Pixel center points of the markers

        print(world_points)
        print(image_points)

        # Compute homography (Perspective Transformation)
        self.H, _ = cv2.findHomography(image_points, world_points) #This serves to compute image coord into real point

    def get_inverse_homography(self):
        """Returns the inverse of the homography matrix for computing pixel coordinates from real points"""
        # Compute inverse homography for mapping back to image space
        return np.linalg.inv(self.H) 

    # Function to transform image coordinates to real-world coordinates
    def transform_to_real_world(self, x, y):
        img_coords = np.array([[x, y, 1]], dtype=np.float32).T
        real_coords = np.dot(self.H, img_coords)
        real_coords /= real_coords[2]  # Normalize
        return real_coords[0][0], real_coords[1][0]

    # Function to transform real-world coordinates to image coordinates
    def transform_to_image_coords(self, x, y, H_inv):
        real_coords = np.array([[x, y, 1]], dtype=np.float32).T
        img_coords = np.dot(H_inv, real_coords)
        img_coords /= img_coords[2]  # Normalize
        return int(img_coords[0][0]), int(img_coords[1][0])

    def set_mode(self, mode):
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

    # Function to rotate a vector by a given angle
    def rotate_vector(self, vector, angle_degrees):
        angle_radians = np.radians(angle_degrees)
        rotation_matrix = np.array([
            [np.cos(angle_radians), -np.sin(angle_radians)],
            [np.sin(angle_radians),  np.cos(angle_radians)]
        ])
        return np.dot(rotation_matrix, vector)

    def polygon_area_cm2(self, world_points):
        """
        Compute area in cm² using shoelace formula.
        world_points: list of (x, y) tuples in cm
        """
        pts = np.array(world_points)
        x = pts[:, 0]
        y = pts[:, 1]
        area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
        return area

    def polygon_perimeter_cm(self, world_points):
        """
        Compute the perimeter of a polygon given its vertices in cm.
        :param world_points: list of (x, y) tuples in cm
        :return: perimeter in cm
        """
        pts = np.array(world_points)
        diffs = np.diff(np.vstack([pts, pts[0]]), axis=0)  # close the polygon loop
        distances = np.linalg.norm(diffs, axis=1)
        return np.sum(distances)


    def image_interaction(self, event, x, y, flags, param):
        """Mouse callback function to handle different actions based on the mode."""
        if event == cv2.EVENT_RBUTTONDOWN: #Close contour
            # vertices = np.array(self.clicked_points, dtype=np.int32).reshape(-1, 1, 2) #transform from list [(,), (,),..] to array [[,], [,],..]  of shape ROWSx1x2 
            # cv2.polylines(self.display_image, vertices, True, (255,0,0), 2)
            # contour_area = cv2.contourArea(vertices)
            # contour_perimeter = cv2.arcLength(vertices, True)

            # Convert pixel points to real-world using homography
            pts = np.array(self.clicked_points, dtype=np.float32)
            pts_homogeneous = cv2.perspectiveTransform(pts.reshape(-1, 1, 2), self.H)
            world_points = [tuple(pt[0]) for pt in pts_homogeneous]

            # Compute perimeter in cm
            self.perimeter_cm = self.polygon_perimeter_cm(world_points)
            print(f"Perimeter: {self.perimeter_cm:.2f} cm")

            # Compute area in cm²
            self.area_cm = self.polygon_area_cm2(world_points)
            print(f"Polygon Area: {self.area_cm:.2f} cm²")

            # Draw the filled polygon on a transparent overlay
            disp_pts = np.array(
                [[int(x * self.scale_factor), int(y * self.scale_factor)] for (x, y) in self.clicked_points],
                np.int32
            )

            overlay = self.display_image.copy()
            cv2.polylines(overlay, [disp_pts], isClosed=True, color=(0, 255, 0), thickness=2)
            cv2.fillPoly(overlay, [disp_pts], (0, 255, 0))
            self.display_image = cv2.addWeighted(overlay, 0.5, self.display_image, 1 - 0.5, 0)

            # Optionally display text
            centroid = np.mean(disp_pts, axis=0).astype(int)
            cv2.putText(self.display_image, f"{self.area_cm:.2f} cm2", tuple(centroid),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)           


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
                    x1, y1 = self.transform_to_real_world(self.clicked_points[0][0], self.clicked_points[0][1]) 
                    x2, y2 = self.transform_to_real_world(self.clicked_points[1][0], self.clicked_points[1][1])
                    print(f"Real-world coordinates: ", x1, y1)

                    # Compute Euclidean distance
                    distance_cm = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                    print(f"Real-world distance: {distance_cm:.2f} cm")

                    # Reset for next selection
                    self.clicked_points.clear()

                    #TODO: Print distance in image: calibration check


            elif self.mode == "points_def":
                clicked_point = (x, y)
                print(f"Selected pixel: {clicked_point}")
                clicked_point_orig = (orig_x, orig_y)
                # Convert clicked pixel to real-world coordinates
                real_world_center = self.transform_to_real_world(orig_x, orig_y)
                print(f"Real-world coordinates: {real_world_center}")
                print(orig_y)
                print(clicked_point_orig[1])

                # Define a second point 1 cm to the right in real-world coordinates
                real_world_edge = (real_world_center[0] + self.circle_radius, real_world_center[1])
                print(real_world_edge)

                # Compute inverse homography for mapping back to image space
                H_inv = np.linalg.inv(self.H) #Serves to compute pixel coord from real points

                # Convert edge point back to image coordinates
                image_edge = self.transform_to_image_coords(real_world_edge[0], real_world_edge[1], H_inv)

                # Compute pixel radius
                pixel_radius = int(np.linalg.norm(np.array(clicked_point_orig) - np.array(image_edge)))

                # # Map from display image to original image
                # x_displ, y_displ = int(x * scale_factor), int(y * scale_factor)
                # image_point = (x_displ, y_displ)
                pixel_radius_display = int(pixel_radius*self.scale_factor)

                # Draw the circle
                # s = self.display_image.copy()
                cv2.circle(self.display_image, clicked_point, pixel_radius_display, (0, 0, 0), 2)  # Print GT corners in plain image
                # cv2.imshow("Image with Circle", self.display_image)
                cv2.circle(self.trial_image, clicked_point, pixel_radius_display, (0, 0, 0), 2)  # Print in trial image (with the results of the team)

                # Reset for next selection
                self.clicked_points.clear()

                #TODO: Save image

            # elif self.mode == "points_def":
            #     if len(self.clicked_points) == 1:
            #         radius_px = int(2 / self.scale_factor)  # Assuming 2cm converted to pixels
            #         disp_center = (int(orig_x * self.scale_factor), int(orig_y * self.scale_factor))
            #         cv2.circle(self.display_image, disp_center, radius_px, (0, 255, 255), 2)  # Cyan circle


            elif self.mode == "vector":
                if len(self.clicked_points) == 2:
                    p1, p2 = np.array(self.clicked_points[0]), np.array(self.clicked_points[1])
                    print(p1)
                    direction = p2 - p1
                    print(direction)
                    direction = direction / np.linalg.norm(direction)  # Normalize

                    ## Get GT line length
                    # line_length = np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
                    # line_length = 250
                    # print("line length: ", line_length)

                    ## Print first line
                    rotated_direction1 = self.rotate_vector(direction, self.vector_tol)
                    endpoint1 = p1 + rotated_direction1 * self.angle_lines_length

                    ## Second line angle
                    rotated_direction2 = self.rotate_vector(direction, -self.vector_tol) # Rotate this direction by 45º
                    endpoint2 = p1 + rotated_direction2 * self.angle_lines_length # Compute the endpoint

                    # Convert to display coordinates
                    disp_p1 = (int(p1[0] * self.scale_factor), int(p1[1] * self.scale_factor))
                    disp_p2 = (int(p2[0] * self.scale_factor), int(p2[1] * self.scale_factor))
                    disp_endpoint1 = (int(endpoint1[0] * self.scale_factor), int(endpoint1[1] * self.scale_factor))
                    disp_endpoint2 = (int(endpoint2[0] * self.scale_factor), int(endpoint2[1] * self.scale_factor))

                    # Draw original reference line (p1 -> p2) 
                    # cv2.line(self.display_image, disp_p1, disp_p2, (255, 0, 0), 2)  # Blue reference line

                    # Draw rotated lines (+-45º from p1)
                    cv2.line(self.display_image, disp_p1, disp_endpoint1, (0, 0, 0), 2)  # Green rotated line
                    cv2.line(self.display_image, disp_p1, disp_endpoint2, (0, 0, 0), 2)  # Green rotated line

                    # Create semi-transparent shadow
                    overlay = self.display_image.copy()
                    triangle_pts = np.array([disp_p1, disp_endpoint1, disp_endpoint2], np.int32)
                    cv2.fillPoly(overlay, [triangle_pts], (50, 50, 50))  # Dark gray shadow
                    self.display_image = cv2.addWeighted(overlay, 0.5, self.display_image, 1 - 0.5, 0) #0.5 is the opacity

                    ## Print in trial image
                    cv2.line(self.trial_image, disp_p1, disp_endpoint1, (0, 0, 0), 2)  # Green rotated line
                    cv2.line(self.trial_image, disp_p1, disp_endpoint2, (0, 0, 0), 2)  # Green rotated line
                    overlay = self.trial_image.copy()
                    triangle_pts = np.array([disp_p1, disp_endpoint1, disp_endpoint2], np.int32)
                    cv2.fillPoly(overlay, [triangle_pts], (50, 50, 50))  # Dark gray shadow
                    self.trial_image = cv2.addWeighted(overlay, 0.4, self.trial_image, 1 - 0.4, 0) #0.5 is the opacity


                    # Reset for next selection
                    self.clicked_points.clear()
    
            elif self.mode == "draw_contour":
                if len(self.clicked_points) > 1:
                    length = len(self.clicked_points)
                    print(len(self.clicked_points))
                    print(self.clicked_points[length-1])
                    ##Draw line between current and past points
                    p1, p2 = np.array(self.clicked_points[length-2]), np.array(self.clicked_points[length-1])
                    distance_px = np.linalg.norm(p2 - p1)
                    print(f"Distance (pixels): {distance_px:.2f}")

                    # Convert to display coordinates and draw line
                    disp_p1 = (int(p1[0] * self.scale_factor), int(p1[1] * self.scale_factor))
                    disp_p2 = (int(p2[0] * self.scale_factor), int(p2[1] * self.scale_factor))
                    cv2.line(self.display_image, disp_p1, disp_p2, (0, 128, 255), 2)  #(255, 255, 0) Yellow line 
                    # if close_contour: #Close contour
                    #     # pts = vertices.reshape((-1,1,2))
                    #     cv2.polylines(img, clicked_points, True, (255,0,0), 2)
                    #     contour_area = cv2.contourArea(vertices)
                    #     contour_perimeter = cv2.arcLength(vertices, True)

            # elif self.mode == "draw_contour": 
            #     cv2.circle(self.display_image, (x, y), 3, (0, 128, 255), -1)

            # Show updated image
            cv2.imshow("Interactive Drawing", self.display_image)
            

    def run(self, img_msg):
        """Main function to run the interactive window."""
        cv2.namedWindow("Interactive Drawing", cv2.WINDOW_NORMAL)
        cv2.setMouseCallback("Interactive Drawing", self.image_interaction)

        # print("Press '1' for Distance Mode, '2' for Circle Mode, '3' for Angle Mode.")
        
        while True:
            cv2.imshow("Interactive Drawing", self.display_image)
            key = cv2.waitKey(1)
            
            if key == 27:  # ESC to exit
                break
            elif key == ord('1'):
                self.set_mode("distance")
            elif key == ord('2'):
                self.set_mode("circle")
            elif key == ord('3'):
                self.set_mode("angle")

        cv2.destroyAllWindows()



