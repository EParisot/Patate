from time import sleep
import RPi.GPIO as GPIO
from picamera.array import PiRGBArray
from picamera import PiCamera
#debug####
import cv2
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
speeds = [0, 0]

def Forward(speeds, delta):
    if speeds[0] != speeds[1]:
        if speeds[0] > speeds[1]:
            speeds[1] = speeds[0]
        else:
            speeds[0] = speeds[1]
    elif speeds[0] + delta <= 100.0 and speeds[1] + delta <= 100.0:
        speeds[0] = speeds[0] + delta
        speeds[1] = speeds[1] + delta
    GPIO.output(MOT1b, GPIO.LOW)
    GPIO.output(MOT2b, GPIO.LOW)
    GPIO.output(MOT1f, GPIO.HIGH)
    GPIO.output(MOT2f, GPIO.HIGH)
    MOT1v.start(speeds[0])
    MOT2v.start(speeds[1])
    return (speeds)

def Brake(speeds, delta):
    if speeds[0] > delta and speeds[1] > delta:
        speeds[0] = speeds[0] - delta
        speeds[1] = speeds[1] - delta
    MOT1v.ChangeDutyCycle(speeds[0])
    MOT2v.ChangeDutyCycle(speeds[1])
    return (speeds)

def Stop():
    MOT1v.stop()
    MOT2v.stop()
    return ([0, 0])

def TurnR(speeds, delta):
    if speeds[0] + delta < 100.0:
        speeds[0] = speeds[0] + delta
        MOT1v.ChangeDutyCycle(speeds[0])
    elif speeds[1] - delta > 0.0:
        speeds[1] = speeds[1] - delta
        MOT2v.ChangeDutyCycle(speeds[1])
    return (speeds)

def TurnL(speeds, delta):
    if speeds[1] + delta < 100.0:
        speeds[1] = speeds[1] + delta
        MOT2v.ChangeDutyCycle(speeds[1])
    elif speeds[0] - delta > 0.0:
        speeds[0] = speeds[0] - delta
        MOT1v.ChangeDutyCycle(speeds[0])
    return (speeds)

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
##  # show the frame
  cv2.imshow("Frame", img)
  key = cv2.waitKey(1) & 0xFF
##  # Clear the stream
  rawCapture.truncate(0)
##  # if 'q' key pressed, break loop
  if key == ord("p"):
    break
# Control example :
  elif key == ord("z"):
    speeds = Forward(speeds, 20)
  elif key == ord("s"):
    speeds = Brake(speeds, 20)
  elif key == ord("d"):
    speeds = TurnR(speeds, 20)
  elif key == ord("q"):
    speeds = TurnL(speeds, 20)

# IA here ##############################################



#Stop the machine and release GPIO Pins#################
Stop()
GPIO.cleanup()
