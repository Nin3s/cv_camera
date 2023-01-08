import cv2
import numpy as np
from datetime import datetime

camera = cv2.VideoCapture(0)

useGrayScale = False

# Test function
def process_click(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        if y > button[0] and y < button[1] and x > button[2] and x < button[3]:
            print("here")

img_counter = 0

# Create a window to apply various effects onto a photo
cv2.namedWindow("Control")
cv2.setMouseCallback('Control', process_click)

button = [20,60,50,250]

control_image = np.zeros((80, 300), np.uint8)
control_image[button[0]:button[1],button[2]:button[3]] = 180
cv2.putText(control_image, 'Grayscale',(50,50),cv2.FONT_HERSHEY_PLAIN, 2,(0),3)

while True:
    (grabbed, frame) = camera.read()
    frame = cv2.flip(frame, 1)
    if not grabbed:
        break

    # Display output
    cv2.putText(frame, str(datetime.now()), (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow("Camera", frame)
    cv2.imshow('Control', control_image)

    k = cv2.waitKey(1)
    img_name = "opencv_frame_{}.png".format(img_counter)
    
    if k == ord("q"):
        break
    elif k == ord(" "):
        if useGrayScale:
            grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow("Camera - Gray", grayFrame)
            cv2.imwrite(img_name, grayFrame)
        else:
            cv2.imshow("{}".format(img_name), frame)
            cv2.imwrite(img_name, frame)
        print("{} saved in current directory".format(img_name))
        img_counter += 1
    elif k == ord("1"):
        if not useGrayScale:
            useGrayScale = True
            print("Grayscale is on")
        else:
            useGrayScale = False
            print("Grayscale is off")

camera.release()
cv2.destroyAllWindows()