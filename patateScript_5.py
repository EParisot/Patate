from time import sleep
import RPi.GPIO as GPIO
from picamera import PiCamera
from picamera.array import PiRGBArray
from keras.models import load_model
import numpy as np
import sys
#####################################

# Load Model(s):
if len(sys.argv) > 1:
  if len(sys.argv) == 2:
    model = load_model(sys.argv[1])
  elif len(sys.argv) == 3:
    model = load_model(sys.argv[1])
    model_a = load_model(sys.argv[2])
    
print("Models Loaded")

#init GPIO with BCM numberings
GPIO.setmode(GPIO.BCM)
#init every used pins
GPIO.setup(23, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

#set controls
POW = GPIO.PWM(18, 50)
DIR = GPIO.PWM(23, 50)

# Video settings
camera = PiCamera()
camera.resolution = (160, 128)
camera.framerate = 60
camera.hflip = True
camera.vflip = True
rawCapture = PiRGBArray(camera, size=(160, 128))

# Starting loop
print("Ready ! (press Ctrl+C to start/stop)...")
try:
  while True:
    pass
except KeyboardInterrupt:
  pass


# Init speeds and memory
SPEED_NORMAL = 6.8 # 6.7
SPEED_FAST = 6.6   # 6.65
speed = SPEED_NORMAL
direction = 7

# Init engines
POW.start(0)
DIR.start(0)
POW.ChangeDutyCycle(speed)


preds_a = [1]

try:
##  # Capture frames
  
    if len(sys.argv) == 1:
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
      ##  # Grab Numpy Array
          img = frame.array
          image = np.array([img[40:, :, :]])
      ##  # Model prediction
          preds = model.predict(image)
          preds = np.argmax(preds, axis=1)
      ##  # Action
          if preds == 0:
              direction = 4
          elif preds == 1:
              direction = 5.5
          elif preds == 2:
              direction = 7
          elif preds == 3:
              direction = 8.5
          elif preds == 4:
              direction = 10
          DIR.ChangeDutyCycle(direction)
      ##  # Clear the stream
          image = np.delete(image, 0)
          rawCapture.truncate(0)

    elif len(sys.argv) == 2:
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
      ##  # Grab Numpy Array
          img = frame.array
          image = np.array([img[40:, :, :]])
      ##  # Model prediction
          preds = model.predict(image)
          preds = np.argmax(preds, axis=1)
      ##  # Action
          if preds == 0:
              speed = SPEED_NORMAL
              direction = 4
          elif preds == 1:
              speed = SPEED_NORMAL
              direction = 5.5
          elif preds == 2:
              image_a = np.array([img[40:58, :, :]])
              preds_a = np.argmax(model_a.predict(image_a), axis=1)
              if preds_a == 1:
                  speed = SPEED_FAST
              else:
                  speed = SPEED_NORMAL
              direction = 7
          elif preds == 3:
              speed = SPEED_NORMAL
              direction = 8.5
          elif preds == 4:
              speed = SPEED_NORMAL
              direction = 10
          POW.ChangeDutyCycle(speed)
          DIR.ChangeDutyCycle(direction)
      ##  # Clear the stream
          image = np.delete(image, 0)
          rawCapture.truncate(0)
except KeyboardInterrupt:
  pass

# Stop the machine and release GPIO Pins
POW.stop(0)
DIR.stop(7)
print("Stop")
GPIO.cleanup()
