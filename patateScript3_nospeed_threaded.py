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

from PIL import Image
frame = vs.read()
img = Image.fromarray(frame)
img.save("test.png")


# Starting loop
print("Ready ! press CTRL+C to START/STOP :")
try:
    while True:
        pass
except KeyboardInterrupt:
    pass

# Handle START/STOP event
try:
    head = H_UP
    speed = SPEED_NORMAL
    pwm.set_pwm(1, 0, speed)
    # loop over some frames...this time using the threaded stream
    while True:
            # grab the frame from the threaded video stream 
            frame = vs.read()
            image = np.array([frame]) / 255.0
            ##  # Model prediction
            preds_raw = model.predict(image)
            preds = np.argmax(preds_raw, axis=1)
            ##  # Action
            if preds == 0:
                direction = DIR_L_M
            elif preds == 1:
                direction = DIR_C
            elif preds == 2:
                direction = DIR_R_M
            ##  # Apply values to engines
            pwm.set_pwm(0, 0, direction)
             # Move Head
            pwm.set_pwm(2, 0, head)

except:
    pass

# Stop the machine
pwm.set_pwm(0, 0, 0)
pwm.set_pwm(1, 0, 0)
pwm.set_pwm(2, 0, 0)
vs.stop()
print("Stop")
