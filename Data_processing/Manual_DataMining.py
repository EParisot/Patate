import time
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2

from const import *
#############################################

# Setup Camera
camera = PiCamera()
camera.resolution = IM_SIZE
camera.framerate = 60
#camera.color_effects = (128,128)
rawCapture = PiRGBArray(camera, size = IM_SIZE)

# Loop over camera frames
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # convert img as Array
    image = frame.array
    # kind of 'wait for key'
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        rawCapture.truncate(0)
        break
    elif key == ord("p"):
        picname = "/home/pi/Documents/Patate/Pics/Manual/" + str(time.time()) + ".jpg"
        # take a pic
        cv2.imwrite(picname, image)
        print("snap : " + picname)
    # Show image
    cv2.imshow("DataSet Mining", image)
    # Clean image before the next comes
    rawCapture.truncate(0)

