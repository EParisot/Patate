import time
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
#############################################

# Setup Camera
camera = PiCamera()
camera.resolution = (160, 96)
camera.framerate = 60
camera.hflip = True
camera.vflip = True
rawCapture = PiRGBArray(camera, size = (160, 96))


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
        picname = "/home/pi/Documents/Patate/Pics/Auto/" + str(time.time()) + ".jpg"
        # take a pic
        cv2.imwrite(picname, image)
        print("snap : " + picname)
    # Show image + infos
    cv2.putText(image, "label = ", (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0, 220, 0], 1)
    cv2.imshow("DataSet Mining", image)
    # Clean image before the next comes
    rawCapture.truncate(0)


