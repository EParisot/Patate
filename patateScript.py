from time import sleep
import RPi.GPIO as GPIO
from picamera import PiCamera
from picamera.array import PiRGBArray
from keras.models import load_model
import numpy as np
#####################################

# Load Model:
model = load_model('model-1x3.h5')
model_a = load_model('model-anticipation.h5')
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
tg = 10
speed = 0
direction = 7

# Init engines
POW.start(0)
DIR.start(0)
POW.ChangeDutyCycle(tg)

last = 1
preds_a = [1]

try:
##  # Capture frames
  for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
##  # Grab Numpy Array
    img = frame.array
    image = np.array([img[50:, :, :]])
##  # Model prediction
    preds = model.predict(image)
    preds = np.argmax(preds, axis=1)
##  # Filter
    print(str(last))
    if (last - preds)*(last - preds) == 4:
        preds = 3
##  # Action
    if preds == 0:
        speed = 5
        direction = 4
    elif preds == 1:
        image_a = np.array([img[40:58, :, :]])
        preds_a = np.argmax(model_a.predict(image_a), axis=1)
        if preds_a == 0:
          speed = 10
        else:
          speed = 5
        direction = 7
    elif preds == 2:
        speed = 5
        direction = 10
    elif preds == 3:
        speed = 5
        direction = 7
    POW.ChangeDutyCycle(tg + speed)
    DIR.ChangeDutyCycle(direction)
    print(str(preds))
##  # Set memory
    last = preds
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
