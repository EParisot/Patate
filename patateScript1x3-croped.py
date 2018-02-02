from time import sleep
import RPi.GPIO as GPIO
from picamera import PiCamera
from picamera.array import PiRGBArray
from keras.models import load_model
import numpy as np
#####################################

# Load Model:
model = load_model('model-1x3-croped-all.h5')
print("Model Loaded")

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

# Video here ############################################
camera = PiCamera()
camera.resolution = (160, 128)
camera.framerate = 60
camera.hflip = True
camera.vflip = True
rawCapture = PiRGBArray(camera, size=(160, 128))

# Start loop
print("Ready ! (press Ctrl+C to start/stop)...")
try:
  while True:
    pass
except KeyboardInterrupt:
  pass

GPIO.output(MOT1f, 1)
GPIO.output(MOT2f, 1)
MOT1v.start(0)
MOT2v.start(0)
speed = 15

try:
### Capture frames examples
  for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
##  # grab Numpy Array
    img = frame.array
    image = np.array([img[70:, :, :]])
    preds = model.predict(image)
    preds = np.argmax(preds[0], axis=0)
    if preds == 0:
        GPIO.output(MOT1f, 0)
        GPIO.output(MOT1b, 1)
        GPIO.output(MOT2f, 1)
        GPIO.output(MOT2b, 0)
        v1 = 3 * speed
        v2 = 3 * speed
    elif preds == 1:
        GPIO.output(MOT1f, 1)
        GPIO.output(MOT1b, 0)
        GPIO.output(MOT2f, 1)
        GPIO.output(MOT2b, 0)
        v1 = speed
        v2 = speed
    elif preds == 2:
        GPIO.output(MOT1f, 1)
        GPIO.output(MOT1b, 0)
        GPIO.output(MOT2f, 0)
        GPIO.output(MOT2b, 1)
        v1 = 3 * speed
        v2 = 3 * speed
    MOT1v.ChangeDutyCycle(v1)
    MOT2v.ChangeDutyCycle(v2)
    print("L = " + str(v1) + " - R = " + str(v2))
##  # Clear the stream
    image = np.delete(image, 0)
    rawCapture.truncate(0)
except KeyboardInterrupt:
  pass

MOT1v.stop(0)
MOT2v.stop(0)

#Stop the machine and release GPIO Pins#################
print("Stop")
GPIO.cleanup()
