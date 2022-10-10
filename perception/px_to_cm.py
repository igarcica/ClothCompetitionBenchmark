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
img = cv2.imread('rulebook/aruco_rot.jpg')
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
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50)

# Get Aruco marker
corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)

# Draw polygon around the marker
int_corners = np.int0(corners)
cv2.polylines(img, int_corners, True, (0, 255, 0), 5)
cv2.imshow('aruco', img)
cv2.waitKey(0)

# Aruco Perimeter
aruco_perimeter = cv2.arcLength(corners[0], True)
print("Aruco pixels: ", aruco_perimeter)

# Pixel to cm ratio
pixel_cm_ratio = aruco_perimeter / 20 # 20 is the Aruco perimeter in cm
print("Pixel/centimeter ratio: ", pixel_cm_ratio) #Pixels/cm

#writer.writerow(pixel_cm_ratio)

##Aruco width
#aruco_width = aruco_perimeter/4
#print("Aruco witdh: ", aruco_width)
#pixel_cm_ratio = aruco_width/5
#print(pixel_cm_ratio)

#Aruco area
aruco_area = cv2.contourArea(corners[0])
print("Aruco area: ", aruco_area)
pixel_cm_ratio_area = aruco_area / 25 # 20 is the Aruco perimeter in cm
print("Pixel2/centimer2 ratio (Area): ", pixel_cm_ratio_area) #Pixels2/cm2

#writer.writerow(pixel_cm_ratio_area)

# Debug
#x,y,w,h = cv2.boundingRect(corners[0])
#rect_area = w*h
#print("Rect: ", rect_area)
#print(rect_area/pixel_cm_ratio)
#print(w)
#print(w/pixel_cm_ratio)
#print(h)
#print(h/pixel_cm_ratio)
#pixel_cm_ratio = rect_area / 25
#print("RAtio: ", pixel_cm_ratio)
#print(rect_area)
#print(rect_area/pixel_cm_ratio)
#print(w)
#print(w/pixel_cm_ratio)
#print(h)
#print(h/pixel_cm_ratio)


#################################
## Draw objects boundaries
#for cnt in contours:
#    # Get rect
#    rect = cv2.minAreaRect(cnt)
#    (x, y), (w, h), angle = rect
#    # Get Width and Height of the Objects by applying the Ratio pixel to cm
#    object_width = w / pixel_cm_ratio
#    object_height = h / pixel_cm_ratio
#
#    cv2.putText(img, "Width {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
#    cv2.putText(img, "Height {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)

#Tener en cuenta que sea un template que pueda caber en una camara puesta cerca de la mesa (deberia coger un flat cloth)

## REFS
#https://pysource.com/2021/05/28/measure-size-of-an-object-with-opencv-aruco-marker-and-python

