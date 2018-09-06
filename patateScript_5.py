from time import sleep
import Adafruit_PCA9685
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
  else:
    print("usage: python patateScript_5.py [path to model.h5]")
    
print("Models Loaded")

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


# Init speeds
SPEED_NORMAL = 320#6.8 # 6.8
SPEED_FAST = 315#6.65   # 6.65

DIR_L_M = 245
DIR_L = 307
DIR_C = 328
DIR_R = 348
DIR_R_M = 409

speed = SPEED_FAST
direction = DIR_C

# Init engines
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)


preds_a = [1]

try:
##  # Capture frames
  
    if len(sys.argv) == 2:
        pwm.set_pwm(1, 0, SPEED_NORMAL)
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            ##  # Grab Numpy Array
            img = frame.array
            image = np.array([img[40:, :, :]])
            ##  # Model prediction
            preds = model.predict(image)
            preds = np.argmax(preds, axis=1)
            ##  # Action
            if preds == 0:
                direction = DIR_L_M
            elif preds == 1:
                direction = DIR_L
            elif preds == 2:
                direction = DIR_C
            elif preds == 3:
                direction = DIR_R
            elif preds == 4:
                direction = DIR_R_M
                
            pwm.set_pwm(0, 0, direction)

            ##  # Clear the stream
            image = np.delete(image, 0)
            rawCapture.truncate(0)

    elif len(sys.argv) == 3:
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
                direction = DIR_L_M
            elif preds == 1:
                speed = SPEED_NORMAL
                direction = DIR_L
            elif preds == 2:
                image_a = np.array([img[40:58, :, :]])
                preds_a = np.argmax(model_a.predict(image_a), axis=1)
                if preds_a == 1:
                    speed = SPEED_FAST
                else:
                    speed = SPEED_NORMAL
                direction = DIR_C
            elif preds == 3:
                speed = SPEED_NORMAL
                direction = DIR_R
            elif preds == 4:
                speed = SPEED_NORMAL
                direction = DIR_R_M
                
            pwm.set_pwm(0, 0, direction)
            pwm.set_pwm(1, 0, speed)
            
            ##  # Clear the stream
            image = np.delete(image, 0)
            rawCapture.truncate(0)
except KeyboardInterrupt:
    pass

# Stop the machine and release GPIO Pins
pwm.set_pwm(0, 0, 0)
pwm.set_pwm(1, 0, 0)
print("Stop")
