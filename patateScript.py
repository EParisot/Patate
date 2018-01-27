from time import sleep
import RPi.GPIO as GPIO
from picamera.array import PiRGBArray
from picamera import PiCamera
from keras.models import load_model
#debug####
import cv2
#####################################

# Load Model:
load_model('test_model.h5')

#init GPIO with BCM numberings
GPIO.setmode(GPIO.BCM)

#init every used pins
GPIO.setup(12, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)

#set vars
MOT1v = GPIO.PWM(12, 50)
MOT1f = 19
MOT1b = 13
MOT2v = GPIO.PWM(16, 50)
MOT2f = 21
MOT2b = 20
speeds = [0, 0]

# Video here ############################################
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 60
camera.hflip = True
camera.vflip = True
rawCapture = PiRGBArray(camera, size=(320, 240))
# Allow cam to warmup
sleep(0.1)

### Capture frames examples
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
##  # grab Numpy Array
  img = frame.array
##  # Process images here
  #IA here:
##  # show the frame
  cv2.imshow("Frame", img)
  key = cv2.waitKey(1) & 0xFF
##  # Clear the stream
  rawCapture.truncate(0)
##  # if 'q' key pressed, break loop
  if key == ord("q"):
    break



#Stop the machine and release GPIO Pins#################
Stop()
GPIO.cleanup()
