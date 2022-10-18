# Introduction

Code to annotate corners in images. Using the mouse left button you can select a pixel on an image corresponding to the corner of the cloth.

# Dependencies

- Testes in Ubunto 20
- Python3
- Numpy: ``sudo apt-get install python3-numpy``
- OpenCV: ``sudo apt-get install python3-opencv``
- Pillow: ``sudo apt-get install python3-pil``

# Execution

To generate the Aruco pattern for getting the pixel/centimeter ratio:
``python3 aruco_pattern.py -o "aruco_markers.png" -i 10 -t "DICT_6X6_50" -d 72 -s 50 -m 20 x 3 -y 3``

## Perception task


Inside perception folder

All this scripts can be executed separately to execute their features.

To annotate the corners at the image, run:
``python3 corner_annotation.py``

Corner annotation:
Over image window "Cloth" click on the corresponding corner. A circle of 10px of diameter will appear in the image window "Corner".

Grasping approach vector:
Over image window "Corner" click on the point of the image that correspond to the end of the vector (origin will be the last annotated corner).

### Usage example

In the root folder, run: 
``python3 perception/perception.py -i 'test/IMG_20221007_174231.jpg' -ii 'test/IMG_20221007_174207.jpg' -o 'team2' -tt 1000``

## Manipulation tasks


All this scripts can be executed separately to execute their features.

To set the contour of the cloth, run:
``python3 contour_annotation.py``

To draw the contour, click in sequence the vertices that compose the contour. To close the contour press the mouse right button.

### Usage example

In the root folder, run:
``python3 manipulation/manipulation.py -i 'test/IMG_20221007_174231.jpg' -ii 'test/IMG_20221007_174149.jpg' -o 'team/' -t "f1" -tt 2 -obj "med_towel"``




