from pivideostream import PiVideoStream
from keras.models import load_model
import Adafruit_PCA9685
from const import *
import numpy as np
import sys
import time

#Load model
model = load_model(sys.argv[1])
print("Model loaded")

# Init engines
speed = SPEED_FAST
direction = DIR_C
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

# created a *threaded *video stream, allow the camera sensor to warmup
vs = PiVideoStream().start()
time.sleep(2.0)

# Starting loop
print("Ready ! press CTRL+C to START/STOP :")
try:
    while True:
        pass
except KeyboardInterrupt:
    pass

# Handle START/STOP event
try:
    # loop over some frames...this time using the threaded stream
    while True:
            # grab the frame from the threaded video stream 
            frame = vs.read()
            image = np.array([frame]) / 255.0
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
except:
    pass

# Stop the machine
pwm.set_pwm(0, 0, 0)
pwm.set_pwm(1, 0, 0)
vs.stop()
print("Stop")
