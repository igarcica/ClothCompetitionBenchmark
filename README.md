## Introduction

Code to annotate corners in images. Using the mouse left button you can select a pixel on an image corresponding to the corner of the cloth.

## Dependencies

- Testes in Ubunto 20
- Python3
- Numpy: ``sudo apt-get install python3-numpy``
- OpenCV: ``sudo apt-get install python3-opencv``

## Execution

To annotate the corners at the image, run:
``python3 corner_annotation.py``

Corner annotation:
Over image window "Cloth" click on the corresponding corner. A circle of 10px of diameter will appear in the image window "Corner".

Grasping approach vector:
Over image window "Corner" click on the point of the image that correspond to the end of the vector (origin will be the last annotated corner).

To set the contour of the cloth, run:
``python3 contour_annotation.py``

To draw the contour, click in sequence the vertices that compose the contour. To close the contour press the mouse right button.
