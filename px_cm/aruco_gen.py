import numpy as np
import cv2, PIL
from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

#fig_w_cm = 21
#fig_h_cm = 29.7
#inches_per_cm = 172.54
#fig_w = fig_w_cm*inches_per_cm
#fig_h = fig_h_cm*inches_per_cm
#fig_size=[fig_w, fig_h]
#
fig = plt.figure()
#fig.set_size_inches(fig_size)

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

img = aruco.drawMarker(aruco_dict,1,500)
plt.imshow(img, cmap=mpl.cm.gray, interpolation="nearest")

#fig = plt.figure()
#nx = 4
#ny = 3
#for i in range(1, nx*ny+1):
#    ax = fig.add_subplot(ny,nx,i)
#    img = aruco.drawMarker(aruco_dict,i,700)
#    plt.imshow(img, cmap=mpl.cm.gray, interpolation="nearest")
#    ax.axis("off")
#
##plt.savefig("markers.pdf", dpi=300, orientation="portrait")
plt.savefig("markers.png")
plt.show()
