from time import sleep
import msvcrt
import RPi.GPIO as GPIO
from picamera.array import PiRGBArray
from picamera import PiCamera
#debug####
#import cv2
#####################################
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

def Forward(speed):
  GPIO.output(MOT1b, GPIO.LOW)
  GPIO.output(MOT2b, GPIO.LOW)
  GPIO.output(MOT1f, GPIO.HIGH)
  GPIO.output(MOT2f, GPIO.HIGH)
  MOT1v.start(speed)
  MOT2v.start(speed)
  return (speed)
  
def Brake(speed, delta):
  MOT1v.ChangeDutyCycle(speed - delta)
  MOT2v.ChangeDutyCycle(speed - delta)

def Stop():
  MOT1v.stop()
  MOT2v.stop()
  
def TurnR(speed, ldelta, rdelta):
  MOT1v.ChangeDutyCycle(speed + ldelta)
  MOT2v.ChangeDutyCycle(speed - rdelta)
  
def TurnL(speed, ldelta, rdelta):
  MOT1v.ChangeDutyCycle(speed - ldelta)
  MOT2v.ChangeDutyCycle(speed + rdelta)


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

# Wait for start
print("Press 's' to Start !...")
msvcrt.getch()

# IA here ##############################################
# Control example :
##speed = Forward(speed)
##sleep(1)
##Brake(speed, 20)
##sleep(1)
##Forward(speed)
##sleep(1)
##TurnR(speed, 20, 10)
##sleep(1)
##TurnL(speed, 10, 20)
##sleep(1)
##Stop()

#Stop the machine and release GPIO Pins#################
Stop()
GPIO.cleanup()
