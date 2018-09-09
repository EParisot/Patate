import Adafruit_PCA9685
from picamera import PiCamera
from picamera.array import PiRGBArray
from keras.models import load_model
import numpy as np
import sys
from time import sleep

from Data_processing.const import *
#####################################

# Load Model(s):
if len(sys.argv) > 1:
    if sys.argv[1] == "--d":
        model = load_model(sys.argv[2])
    elif sys.argv[1] == "--sd":
        model = load_model(sys.argv[2])
        model_a = load_model(sys.argv[3])
    elif sys.argv[1] == "--m":
        model = load_model(sys.argv[2])
    else:
        print("usage: python patateScript.py [type] [path(s) to model.h5]\n \
          type: --d : direction only \n\
            \t --sd : speed + direction\n\
            \t --m : multitask\n")
        exit(0)
else:
    print("usage: python patateScript.py [type] [path(s) to model.h5]\n \
          type: --d : direction only \n\
            \t --sd : speed + direction\n\
            \t --m : multitask\n")
    exit(0)
    
print("Model(s) Loaded")

# Video settings
camera = PiCamera()
camera.resolution = (160, 96)
camera.framerate = 60
#camera.hflip = True
#camera.vflip = True
rawCapture = PiRGBArray(camera, size=(160, 96))

# Starting loop
print("Ready ! press CTRL+C to START/STOP :")
try:
  while True:
    pass
except KeyboardInterrupt:
  pass

speed = SPEED_FAST
direction = DIR_C

# Init engines
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

# Handle START/STOP event
try:

    ## # Simple Direction model
    if sys.argv[1] == "--d":
        print("Go ! (dir)")
        pwm.set_pwm(1, 0, SPEED_NORMAL)
        ##  # Capture frames
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            ##  # Grab Numpy Array
            img = frame.array
            image = np.array([img])
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
            ##  # Apply values to engine 
            pwm.set_pwm(0, 0, direction)
            ##  # Clear the stream
            image = np.delete(image, 0)
            rawCapture.truncate(0)
            
    ## # Speed + Direction models
    elif sys.argv[1] == "--sd":
        print("Go ! (speed + dir)")
        ##  # Capture frames
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            ##  # Grab Numpy Array
            img = frame.array
            image = np.array([img])
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
                image_a = np.array([img])
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
            ##  # Apply values to engines 
            pwm.set_pwm(0, 0, direction)
            pwm.set_pwm(1, 0, speed)
            ##  # Clear the stream
            image = np.delete(image, 0)
            rawCapture.truncate(0)

    ## # Multitask model
    elif sys.argv[1] == "--m":
        print("Go ! (multi)")
        ##  # Capture frames
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            ##  # Grab Numpy Array
            img = frame.array
            image = np.array([img])
            ##  # Model prediction
            preds = model.predict(image)
            preds = [np.argmax(pred, axis=1) for pred in preds]
            ##  # Action
            if preds[1] == 0:
                speed = SPEED_NORMAL
                direction = DIR_L_M
            elif preds[1] == 1:
                speed = SPEED_NORMAL
                direction = DIR_L
            elif preds[1] == 2:
                if preds[0] == 1:
                    speed = SPEED_FAST
                else:
                    speed = SPEED_NORMAL
                direction = DIR_C
            elif preds[1] == 3:
                speed = SPEED_NORMAL
                direction = DIR_R
            elif preds[1] == 4:
                speed = SPEED_NORMAL
                direction = DIR_R_M
            ##  # Apply values to engines   
            pwm.set_pwm(0, 0, direction)
            pwm.set_pwm(1, 0, speed)
            ##  # Clear the stream
            image = np.delete(image, 0)
            rawCapture.truncate(0)
            
except:
    # Stop the machine
    pwm.set_pwm(0, 0, 0)
    pwm.set_pwm(1, 0, 0)
    rawCapture.truncate(0)

print("Stop")
