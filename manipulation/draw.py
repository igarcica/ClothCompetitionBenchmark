import cv2
import numpy as np 

drawing = False # true if mouse is pressed
pt1_x , pt1_y = None , None

px_cm_ratio = 9.25054
px_cm_ratio_area = 85.56

# read a colourful image
img = cv2.imread('rulebook/towel.jpg')
print("Image dim: ", img.shape)
scale_percent = 40 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
# resize image
img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

cv2.imshow('Test', img)


# mouse callback function
def line_drawing(event,x,y,flags,param):
    global pt1_x,pt1_y,drawing,vertices

    if event==cv2.EVENT_LBUTTONDOWN:
        drawing=True
        pt1_x,pt1_y=x,y
        vertices = np.array([[x,y]])

    elif event==cv2.EVENT_MOUSEMOVE:
        if drawing==True:
            cv2.line(img,(pt1_x,pt1_y),(x,y),color=(255,255,255),thickness=3)
            pt1_x,pt1_y=x,y
            vertices = np.append(vertices, np.array([[x,y]]), axis=0)
    elif event==cv2.EVENT_LBUTTONUP:
        drawing=False
        cv2.line(img,(pt1_x,pt1_y),(x,y),color=(255,255,255),thickness=3)       
        pts = vertices.reshape((-1,1,2))
        cv2.polylines(img, [pts], True, (0,0,255), 3)
        cv2.imshow('Test', img)
        print("Area (px): ", cv2.contourArea(vertices))
        print("Area (cm): ", cv2.contourArea(vertices)/px_cm_ratio_area)
        print("Perimeter (pc): ", cv2.arcLength(vertices, True))
        print("Perimeter (cm): ", cv2.arcLength(vertices, True)/px_cm_ratio)

#img = np.zeros((512,512,3), np.uint8)
#cv2.namedWindow('test draw')
cv2.setMouseCallback('Test',line_drawing)

while(1):
    cv2.imshow('Test',img)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cv2.destroyAllWindows()


## REFS
#https://stackoverflow.com/questions/28340950/opencv-how-to-draw-continously-with-a-mouse
