import RPi.GPIO as GPIO
import time
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
#############################################

# Setup GPIO Pins
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Start timers
#start_time1 = time.time()
#speed1 = 0
#start_time2 = time.time()
#speed2 = 0

# Setup Camera
camera = PiCamera()
camera.resolution = (160, 128)
camera.framerate = 60
camera.hflip = True
camera.vflip = True
rawCapture = PiRGBArray(camera, size = (160, 120))

# Function called each magnet interuption that
# calculates time between two magnet interuptions
#def callback(channel):
#    global start_time1, speed1, start_time2, speed2
#    if channel == 4:
#        elapsed1 = time.time() - start_time1
#        start_time1 = time.time()
#        speed1 = 0.08 / elapsed1
#    elif channel == 17:
#        elapsed2 = time.time() - start_time2
#        start_time2 = time.time()
#        speed2 = 0.08 / elapsed2

# Track magnet interuptions
#GPIO.add_event_detect(4, GPIO.FALLING, callback=callback, bouncetime=50)
#GPIO.add_event_detect(17, GPIO.FALLING, callback=callback, bouncetime=50)

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
        picname = "/home/pi/Documents/Patate/Pics/raceday2/" + str(time.time()) + ".jpg"
        # take a pic
        cv2.imwrite(picname, image)
        print("snap : " + picname)
    # Show image + infos
#    cv2.putText(image, "L: " + str(round(speed1, 2)) +" - R: " + str(round(speed2, 2)),
#        (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0, 220, 0], 1)
    cv2.imshow("DataSet Mining", image)
    # Clean image before the next comes
    rawCapture.truncate(0)
    # set speeds to 0 if no move during a sec
#    if time.time() - start_time1 > 1:
#        speed1 = 0
#    if time.time() - start_time2 > 1:
#        speed2 = 0

# Clean GPIO Pins
#GPIO.cleanup()

