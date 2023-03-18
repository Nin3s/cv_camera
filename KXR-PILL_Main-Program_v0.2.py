''' 
This is the main program responsible for controlling the Payload Integrated Launch Log (P.I.L.L.)
The PILL is the experimental payload the NASA Student Launch Competition

The following code is proprietary to Knights Experimental Rocketry
'''
print("KXR-PILL_Main-Program Running...")

import smbus2
import adafruit_bno055
import board
import cv2
import numpy as np
from datetime import datetime
from PIL import Image
from gpiozero import Servo
from gpiozero import AngularServo
import time

camera = cv2.VideoCapture(0)

if camera.isOpened() == False:
    print("ERROR: Camera is not operational")
else:
    print("INFO: Camera is functioning")

# Various effects, global variables
useGrayScale = False
flipped = False
useOverlay = False
gifOverlay = False

# This is just used for naming the files
# In the future, we can use the timestamp as our file names
img_counter = 0
i = 0

i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c)
BNO = 0x29
bus = smbus2.SMBus(1)

cam_servo = AngularServo(18, min_angle=-90, max_angle=90, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)
cam_servo.angle = -90
print(cam_servo.angle)

cont_servo = Servo(12)
cont_servo.detach()

def applyFilters(frame):
    global useGrayScale
    global flipped

    if useGrayScale:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if flipped:
        frame = cv2.flip(frame, -1)

    return frame

def doGifOverlay(frame, now):

    global gifOverlay
    global img_counter

    gif = cv2.VideoCapture('bad_news.gif')

    frames = []
    while True:
        ret, gif_frame = gif.read()
        if not ret:
            break

        gif_frame = cv2.resize(gif_frame, (frame.shape[1], frame.shape[0]))
        overlay = cv2.addWeighted(gif_frame, 0.3, frame, 0.5, 0)

        # Check if other effects are on
        overlay = applyFilters(overlay)

        cv2.putText(overlay, now, (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2, cv2.LINE_AA)
        frames.append(overlay)

    frames_pil = [Image.fromarray(f) for f in frames]
    frames_pil[0].save("{}_opencv_gif.gif".format(img_counter), save_all=True, append_images=frames_pil[1:], loop=0)

def takePhoto(frame):
    global useGrayScale
    global flipped
    global useOverlay
    global gifOverlay
    global img_counter
    
    curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if gifOverlay:
        doGifOverlay(frame, curr_time)
    else:
        frame = applyFilters(frame)

        if useOverlay:
            overlay_img = cv2.imread('bad_news_img.png', cv2.COLOR_BGR2GRAY)

            overlay_img = cv2.resize(overlay_img, (640, 480))

            if useGrayScale: # convert to 2 channels, program will fail without it, see Color Channels in the README for more
                gray_img = cv2.cvtColor(overlay_img, cv2.COLOR_BGR2GRAY)
                frame = cv2.addWeighted(frame, 0.4, gray_img, 0.7, 0)
            else:
                frame = cv2.addWeighted(frame, 0.7, overlay_img, 0.4, 0)

        cv2.putText(frame, curr_time, (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.imshow("{}_opencv_img.png".format(img_counter), frame)
        cv2.imwrite("{}_opencv_img.png".format(img_counter), frame)

def runCamera():
    global useGrayScale
    global flipped
    global useOverlay
    global gifOverlay
    global img_counter
    global i
    while True:
        (grabbed, frame) = camera.read()
        frame = cv2.flip(frame, 1) # Mirrors camera output, feel free to remove if you feel like we should have the unmirrored version
        if not grabbed:
            break

        # Display output
        cv2.imshow("Camera", frame)

        k = cv2.waitKey(1)
        #img_name = "opencv_frame_{}.png".format(img_counter)
        
        if k == ord("q"):
            break

        # Toggles effects, print statements are for logging it in the console
        elif i == 1:
            if not useGrayScale:
                useGrayScale = True
                print("Grayscale is on")
            else:
                useGrayScale = False
                print("Grayscale is off")
        elif i == 2:
            if not flipped:
                flipped = True
                print("Output will be flipped 180 degrees")
            else:
                flipped = False
                print("Output will have original orientation")
        elif i == 3:
            if not useOverlay:
                useOverlay = True
                gifOverlay = False
                print("Overlay active")
                print("Gif overlay inactive")
            else:
                useOverlay = False
                print("Overlay inactive")
        elif i == 4: # static overlay (not needed, but here just in case we can't use gif overlay)
            if not gifOverlay:
                gifOverlay = True
                useOverlay = False
                print("Gif overlay active")
                print("Static overlay inactive")
            else:
                gifOverlay = False
                print("Gif overlay inactive")
        elif i == 5:
            print("Clearing all active effects...\n")
            useGrayScale = False
            flipped = False
            useOverlay = False
            gifOverlay = False
            print("Cleared.")
            i = -1

        new_frame = frame
        takePhoto(new_frame)
        img_counter += 1

        time.sleep(30)


    camera.release()
    cv2.destroyAllWindows()

def control_elevator(delay, speed):
    cont_servo.value = speed
    time.sleep(delay)
    cont_servo.detach()
    
def elevator_up():
    control_elevator(5, -1)
    print("Raising Elevator")
    
def elevator_down():
    control_elevator(5, 1)
    print("Lowering Elevator")

def turnto_camera(deg):
    cam_servo.angle = deg
    time.sleep(1)
    print(cam_servo.angle)

def bootUpTest():
    #prints results from POST test on BNO055, telling the user if everything is working or not
    boot_test = bus.read_byte_data(BNO, 0x36)
    print("BNO055 Boot Test", boot_test)
    time.sleep(2)
    print("Prepare for servo test...")
    time.sleep(2)
    elevator_up()
    turnto_camera(-60)
    turnto_camera(-30)
    turnto_camera(0)
    turnto_camera(30)
    turnto_camera(60)
    turnto_camera(90)
    elevator_down()

def preLaunch():
    #reads accelertion until a large spike to recognize launch and thus beginning of launch, then breaks out of loop
    while (True):
        accel = sensor._acceleration
        if accel > 10:
            print("Launch Began!")
            break

def midLaunch():
    #reads acceleration until it becomes negative (changes direction) and thus reaches apogee, then break out of loop
    while (True):
        accel = sensor._acceleration
        if accel < 0:
            print("Apogee Reached!")
            break
    
def endLaunch():
    #reads acceleration and orientation until the acceleration and change in orientation are close to zero, then breaks out of loop
    while (True):
        data = [sensor.acceleration, sensor.gyro]
        if abs(data[0]) < 0.3 and abs(data[1]) < 0.3:
            print("Deploying PILL Camera!")
            elevator_up()
            break


if __name__ == "__main__": main()

def main():
    bootUpTest() #boot up test results
    preLaunch() #determines when rocket launches
    midLaunch() #determines when rocket reaches apogee
    endLaunch() #determines when PILL stops moving and rotating
    runCamera()


if __name__ == "__main__": main()