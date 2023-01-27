import cv2
import numpy as np
from datetime import datetime

camera = cv2.VideoCapture(0)

# Various effects
useGrayScale = False
flipped = False
overlay = False

# This is just used for naming the files
# In the future, we can use the timestamp as our file names
img_counter = 0

while True:
    (grabbed, frame) = camera.read()
    frame = cv2.flip(frame, 1) # Mirrors camera output, feel free to remove if you feel like we should have the unmirrored version
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
            print(new_frame.shape)

        if flipped:
            new_frame = cv2.flip(new_frame, -1)

        if overlay:
            overlay_img = cv2.imread('bad_news_img.png', cv2.COLOR_BGR2GRAY)
            print(overlay_img.shape)

            overlay_img = cv2.resize(overlay_img, (640, 480))

            if useGrayScale: # convert to 2 channels
                b, g, r = cv2.split(overlay_img)
                img = cv2.merge((b,g,r))
                gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                new_frame = cv2.addWeighted(new_frame, 0.5, gray_img, 0.7, 0)
            else:
                new_frame = cv2.addWeighted(new_frame, 0.7, overlay_img, 0.4, 0)

        cv2.putText(new_frame, str(datetime.now()), (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.imshow("{}".format(img_name), new_frame)
        cv2.imwrite(img_name, new_frame)
        print("{} saved in current directory".format(img_name))
        img_counter += 1

    # Toggles effects, print statements are for logging it in the console
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
    elif k == ord("3"):
        if not overlay:
            overlay = True
            print("Overlay active")
        else:
            overlay = False
            print("Overlay inactive")

camera.release()
cv2.destroyAllWindows()