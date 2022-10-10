#!/usr/bin/env python
import numpy as np
import cv2
import math
import csv

##############################
## Generate marker
#cv.Mat markerImage;
#cv.Ptr<cv::aruco::Dictionary> dictionary = cv::aruco::getPredefinedDictionary(cv::aruco::DICT_6X6_50);
#cv.aruco.drawMarker(dictionary, 23, 200, markerImage, 1);
#cv2.imwrite("marker23.png", markerImage);


###############################
#img = cv2.imread('chekered.jpg')
#img = cv2.imread('aruco_markers.png')
#img = cv2.imread('test/IMG_20221007_173630.jpg')
img = cv2.imread('test/IMG_20221007_174231.jpg')
print("Image dim: ", img.shape)
scale_percent = 40 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
# resize image
img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
#img = cv2.resize(img, (840, 1280))
# Load Aruco detector
parameters = cv2.aruco.DetectorParameters_create()
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)

# Get Aruco marker
corners, ids, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)

for (markerCorner, markerID) in zip(corners, ids):
    # extract the marker corners (which are always returned
    # in top-left, top-right, bottom-right, and bottom-left
    # order)
    if(markerID==10 or markerID==12 or markerID==16 or markerID==18):
        corners = markerCorner.reshape((4, 2))
        (topLeft, topRight, bottomRight, bottomLeft) = corners
        #print(corners)
        # convert each of the (x, y)-coordinate pairs to integers
        topRight = (int(topRight[0]), int(topRight[1]))
        bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
        bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
        topLeft = (int(topLeft[0]), int(topLeft[1]))
        # draw the bounding box of the ArUCo detection
        cv2.line(img, topLeft, topRight, (0, 255, 0), 2)
        cv2.line(img, topRight, bottomRight, (0, 255, 0), 2)
        cv2.line(img, bottomRight, bottomLeft, (0, 255, 0), 2)
        cv2.line(img, bottomLeft, topLeft, (0, 255, 0), 2)
        # compute and draw the center (x, y)-coordinates of the
        # ArUco marker
        cX = int((topLeft[0] + bottomRight[0]) / 2.0)
        cY = int((topLeft[1] + bottomRight[1]) / 2.0)
        cv2.circle(img, (cX, cY), 4, (0, 0, 255), -1)
        print(cX,cY)
        # draw the ArUco marker ID on the img
        cv2.putText(img, str(markerID), (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        # show the output img
        cv2.imshow("Frame", img)
        cv2.waitKey(0)
        if(markerID==10):
            topL_x = cX
            topL_y = cY
        if(markerID==12):
            topR_x = cX
            topR_y = cY
        if(markerID==16):
            botL_x = cX
            botL_y = cY
        if(markerID==18):
            botR_x = cX
            botR_y = cY

pts1 = np.float32([[topL_x, topL_y],[topR_x, topR_y],[botL_x, botL_y],[botR_x,botR_y]])
pts2 = np.float32([[0,0],[200,0],[0,200],[200,200]])
#pts2 = np.float32([[0,0],[1080,0],[0,1080],[1080,1080]])
#pts2 = np.float32([[0,0],[270,0],[0,310],[270,310]])
M = cv2.getPerspectiveTransform(pts1,pts2)
print(M)
dst = cv2.warpPerspective(img,M,(200,200))
#dst = cv2.warpPerspective(img,M,(img.shape[1],img.shape[0]))
cv2.imshow('dst', dst)
cv2.waitKey(0)

# Get center Aruco marker
corners, ids, _ = cv2.aruco.detectMarkers(dst, aruco_dict, parameters=parameters)
for (markerCorner, markerID) in zip(corners, ids):
    print("hola")
    if(markerID==14): #center marker
        print("detectado")
        int_corners = np.int0(markerCorner)
        cv2.polylines(dst, int_corners, True, (0, 255, 0), 5)
        cv2.imshow('aruco', dst)
        cv2.waitKey(0)
        
        # Aruco Perimeter
        aruco_perimeter = cv2.arcLength(markerCorner[0], True)
        print("Aruco pixels: ", aruco_perimeter)
        
        # Pixel to cm ratio
        pixel_cm_ratio = aruco_perimeter / 20 # 20 is the Aruco perimeter in cm
        print("Pixel/centimeter ratio: ", pixel_cm_ratio) #Pixels/cm

print("heh")

### Draw polygon around the marker
##int_corners = np.int0(corners)
##cv2.polylines(img, int_corners, True, (0, 255, 0), 5)
##cv2.imshow('aruco', img)
##cv2.waitKey(0)
##
### Aruco Perimeter
##aruco_perimeter = cv2.arcLength(corners[0], True)
##print("Aruco pixels: ", aruco_perimeter)
##
### Pixel to cm ratio
##pixel_cm_ratio = aruco_perimeter / 20 # 20 is the Aruco perimeter in cm
##print("Pixel/centimeter ratio: ", pixel_cm_ratio) #Pixels/cm
##
###writer.writerow(pixel_cm_ratio)
##
####Aruco width
###aruco_width = aruco_perimeter/4
###print("Aruco witdh: ", aruco_width)
###pixel_cm_ratio = aruco_width/5
###print(pixel_cm_ratio)
##
###Aruco area
##aruco_area = cv2.contourArea(corners[0])
##print("Aruco area: ", aruco_area)
##pixel_cm_ratio_area = aruco_area / 25 # 20 is the Aruco perimeter in cm
##print("Pixel2/centimer2 ratio (Area): ", pixel_cm_ratio_area) #Pixels2/cm2
##
###writer.writerow(pixel_cm_ratio_area)
##
### Debug
###x,y,w,h = cv2.boundingRect(corners[0])
###rect_area = w*h
###print("Rect: ", rect_area)
###print(rect_area/pixel_cm_ratio)
###print(w)
###print(w/pixel_cm_ratio)
###print(h)
###print(h/pixel_cm_ratio)
###pixel_cm_ratio = rect_area / 25
###print("RAtio: ", pixel_cm_ratio)
###print(rect_area)
###print(rect_area/pixel_cm_ratio)
###print(w)
###print(w/pixel_cm_ratio)
###print(h)
###print(h/pixel_cm_ratio)
##
##
###################################
#### Draw objects boundaries
###for cnt in contours:
###    # Get rect
###    rect = cv2.minAreaRect(cnt)
###    (x, y), (w, h), angle = rect
###    # Get Width and Height of the Objects by applying the Ratio pixel to cm
###    object_width = w / pixel_cm_ratio
###    object_height = h / pixel_cm_ratio
###
###    cv2.putText(img, "Width {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
###    cv2.putText(img, "Height {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
##
###Tener en cuenta que sea un template que pueda caber en una camara puesta cerca de la mesa (deberia coger un flat cloth)
##
#### REFS
###https://pysource.com/2021/05/28/measure-size-of-an-object-with-opencv-aruco-marker-and-python
##


# https://pyimagesearch.com/2020/12/21/detecting-aruco-markers-with-opencv-and-python/
