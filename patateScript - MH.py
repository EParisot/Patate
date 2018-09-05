from time import sleep
import RPi.GPIO as GPIO
from picamera import PiCamera
from picamera.array import PiRGBArray
from keras.models import load_model
import numpy as np
import keras.backend as K
import h5py
#####################################

# Load Model:
model = load_model('model-MHRaceRich.h5')
#model = load_model('model-MHRace_2.h5')
#model_a = load_model('model-BigDataset-anticipation_Race.h5')
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
SPEED_NORMAL = 6.76 # 6.8
SPEED_FAST = 6.6   # 6.65
speed = SPEED_NORMAL
direction = 7

# Init engines
POW.start(0)
DIR.start(0)
POW.ChangeDutyCycle(speed)

last = 1
#preds_a = [1]

try:
##  # Capture frames
  for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
   # print('speed: ' + str(speed)) ################################################
##  # Grab Numpy Array
    img = frame.array
    image = np.array([img[40:, :, :]])
##  # Model prediction
    preds_dir, preds_speed = model.predict(image)
    preds_dir = np.argmax(preds_dir, axis=1)
    preds_speed = np.argmax(preds_speed, axis=1)
##  # Filter
    #print(str(last))
    if (last - preds_dir)*(last - preds_dir) == 4:
        preds_dir = 3
##  # Action
    if preds_dir == 0:
        direction = 4
    elif preds_dir == 1:
        direction = 7
    elif preds_dir == 2:
        direction = 10
    #elif preds_dir == 3:
    #    direction = 7
    if preds_speed == 0:
      speed = SPEED_NORMAL
    else:
      speed = SPEED_FAST
    POW.ChangeDutyCycle(speed)
    DIR.ChangeDutyCycle(direction)
    #print(str(preds))
##  # Set memory
    last = preds_dir
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
