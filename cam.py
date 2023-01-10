import cv2
import numpy as np
from datetime import datetime

camera = cv2.VideoCapture(0)

# Various effects
useGrayScale = False
flipped = False

# This is just used for naming the files
# In the future, we can use the timestamp as our file names
img_counter = 0

while True:
    (grabbed, frame) = camera.read()
    frame = cv2.flip(frame, 1)
    if not grabbed:
        break

    # Display output
    cv2.imshow("Camera", frame)

    k = cv2.waitKey(1)
    img_name = "opencv_frame_{}.png".format(img_counter)
    
    if k == ord("q"):
        break
    elif k == ord(" "):
        new_frame = frame
        # These if statements apply the desired effects onto our captured frame (new_frame)
        if useGrayScale:
            new_frame = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)

        if flipped:
            new_frame = cv2.flip(new_frame, -1)

        cv2.putText(new_frame, str(datetime.now()), (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow("{}".format(img_name), new_frame)
        cv2.imwrite(img_name, new_frame)
        print("{} saved in current directory".format(img_name))
        img_counter += 1

    elif k == ord("1"):
        if not useGrayScale:
            useGrayScale = True
            print("Grayscale is on")
        else:
            useGrayScale = False
            print("Grayscale is off")
    elif k == ord("2"):
        if not flipped:
            flipped = True
            print("Output will be flipped 180 degrees")
        else:
            flipped = False
            print("Output will have original orientation")

camera.release()
cv2.destroyAllWindows()