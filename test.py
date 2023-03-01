import cv2
from PIL import Image, ImageSequence
import numpy as np

img_counter = 0
gifOverlay = False

camera = cv2.VideoCapture(0)

def doGifOverlay(new_frame):
    gif = cv2.VideoCapture('bad_news.gif')

    frames = []
    while True:
        ret, gif_frame = gif.read()
        if not ret:
            break

        gif_frame = cv2.resize(gif_frame, (new_frame.shape[1], new_frame.shape[0]))
        overlay = cv2.addWeighted(gif_frame, 0.5, new_frame, 0.5, 0)
        frames.append(overlay)

    frames_pil = [Image.fromarray(frame) for frame in frames]
    frames_pil[0].save("test.gif", save_all=True, append_images=frames_pil[1:], loop=0)

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
        doGifOverlay(frame)

    # Toggles effects, print statements are for logging it in the console
    elif k == ord("1"):
        if not gifOverlay:
            gifOverlay = True
            print("overlay is on")
        else:
            gifOverlay = False
            print("overlay is off")

camera.release()
cv2.destroyAllWindows()