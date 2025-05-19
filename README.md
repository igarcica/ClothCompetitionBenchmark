<!-- <div align="center">
  <h1 align="center">Cloth Manipulation and Perception Competition</h1>
</div> -->

<p align="center">
 <a href="https://www.iri.upc.edu/groups/perception/ClothManipulationChallenge/">
  <img width="360" src="competition_logo.jpg?raw=true" alt="Logo" />
 </a>
 <br>
</p>

This repository contains the code for the evaluation of the [Cloth Manipulation and Perception Competition](https://www.iri.upc.edu/groups/perception/ClothManipulationChallenge/), held in IROS 2022 and ICRA 2023.


Contact: Irene Garcia-Camacho (igarcia@iri.upc.edu)



## Getting started

The respository includes the necessary packages to evaluate the performance of the competition tasks of both tracks:

- Perception
- Manipulation
    - Task 2.1. Unfolding
    - Task 2.2. Folding


The package has the following structure:

- **/IROS2022** includes the team's results and scoring of the teams that participated in the **first edition** of the competition in **IROS 2022**. 
- **/ICRA2023** includes the team's results and scoring of the teams that participated in the **second edition** of the competition in **ICRA 2023**. 
- **/perception** contains the script to assess the tasks of the Perception track.
- **/manipulation** contains the script to assess the tasks of the Manipulation track.
- **/px_to_cm** contains the script to obtain the Homography matrix to compute the pixel to centimeter transformation.
    <!-- - *px_to_cm.py*: Script to obtain the pixel to centimeter ratio for obtaining a common unit for all camera brands and setups. -->

<!-- Code to annotate corners in images. Using the mouse left button you can select a pixel on an image corresponding to the corner of the cloth. -->

<!-- # Dependencies

- Tested in Ubuntu 20
- Python3
- Numpy: ``sudo apt-get install python3-numpy``
- OpenCV: ``sudo apt-get install python3-opencv``
- Pillow: ``sudo apt-get install python3-pil`` -->

## Execution

<!-- To generate the Aruco pattern for getting the pixel/centimeter ratio:
``python3 aruco_pattern.py -o "aruco_markers.png" -i 10 -t "DICT_6X6_50" -d 72 -s 50 -m 20 x 3 -y 3`` -->

### Perception task

<!-- All this scripts can be executed separately to execute their features. -->

To annotate the corners at the image, run:
<!-- ``python3 corner_annotation.py`` -->
``python3 perception/perception.py``

Corner annotation:
Over image window click on the corresponding corner, a circle of 2cm of diameter will appear. Then, click again on the point you want to define the grasping approach vector to draw the angle tolerance. 

<!-- Grasping approach vector:
Over image window "Corner" click on the point of the image that correspond to the end of the vector (origin will be the last annotated corner). -->

<!-- ### Usage example

In the root folder, run:
 
``python3 perception/perception.py -i 'pattern.jpg' -p 'towel.jpg' -ii 'towel_markers.jpg' -o 'test' -tt 1000`` -->

### Manipulation tasks

To define the contour of the cloth, run:
``python3 manipulation/manipulation.py``

Draw the contour by clicking in sequence the vertices that compose the contour. To close the contour press the mouse right button.

<!-- ### Usage example

In the root folder, run:

``python3 manipulation/manipulation.py -i 'pattern.jpg' -x 'towel.jpg' -ii 'towel.jpg' -o 'team/' -t "u" -tt 2 -obj "med_towel"`` -->

<!-- 
# Competition scoring

## IDLab-AIRO team

### Perception task

``python3 perception/perception.py -i 'aruco_gent.png' -ii 'trial_input_1.png' -o 'IDLab-AIRO' -tt 1``


## UMich team

## AIS-Shinshu team -->


