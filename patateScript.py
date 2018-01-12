from time import sleep
import RPi.GPIO as GPIO
from picamera.array import PiRGBArray
from picamera import PiCamera
#debug####
import cv2
###########
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
speed = 50

def Forward(speed):
  GPIO.output(MOT1b, GPIO.LOW)
  GPIO.output(MOT2b, GPIO.LOW)
  GPIO.output(MOT1f, GPIO.HIGH)
  GPIO.output(MOT2f, GPIO.HIGH)
  MOT1v.start(speed)
  MOT2v.start(speed)
  
def Brake(speed):
  MOT1v.ChangeDutyCycle(speed - 20)
  MOT2v.ChangeDutyCycle(speed - 20)

def Stop():
  MOT1v.stop()
  MOT2v.stop()
  
def TurnR(speed):
  MOT1v.ChangeDutyCycle(speed - 10)
  MOT2v.ChangeDutyCycle(speed + 20)
  
def TurnL(speed):
  MOT1v.ChangeDutyCycle(speed + 20)
  MOT2v.ChangeDutyCycle(speed - 10)


# Video here ############################################
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 30
camera.hflip = True
camera.vflip = True
rawCapture = PiRGBArray(camera, size=(320, 240))
# Allow cam to warmup
sleep(0.1)

### Capture frames examples
##for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
##  # grab Numpy Array
##  img = frame.array
##  # Process images here
##  # show the frame
##  cv2.imshow("Frame", img)
##  key = cv2.waitKey(1) & 0xFF
##  # Clear the stream
##  rawCapture.truncate(0)
##  # if 'q' key pressed, break loop
##  if key == ord("q"):
##    break

# IA here ##############################################

##Forward(speed)
##sleep(1)
##Brake(speed)
##sleep(1)
##Forward(speed)
##sleep(1)
##TurnR(speed)
##sleep(1)
##TurnL(speed)
##sleep(1)
##Stop()

#Stop the machine and release GPIO Pins#################
Stop()
GPIO.cleanup()
