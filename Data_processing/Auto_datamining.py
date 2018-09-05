try:
    import cv2
except:
    print("run 'workon cv' before you start the script")
    exit(0)

import RPi.GPIO as GPIO
import time
from picamera import PiCamera
from picamera.array import PiRGBArray

import sys
import threading

#############################################

if len(sys.argv) == 2:
    delay = [float(sys.argv[1])]

label = [-1, 2]

#init GPIO with BCM numberings
GPIO.setmode(GPIO.BCM)
#init every used pins
GPIO.setup(23, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
#set controls
POW = GPIO.PWM(18, 50)
DIR = GPIO.PWM(23, 50)

# Init speeds
SPEED_NORMAL = 6.76 # 6.8
SPEED_FAST = 6.6   # 6.65
speed = SPEED_NORMAL

# Init directions
DIR_L_M = 5
DIR_L = 6.5
DIR_C = 7
DIR_R = 7.5
DIR_R_M = 9
direction = DIR_C

# Loop over camera frames
def videoLoop(delay):
    # Setup Camera
    camera = PiCamera()
    camera.resolution = (160, 128)
    camera.framerate = 60
    camera.hflip = True
    camera.vflip = True
    rawCapture = PiRGBArray(camera, size = (160, 120))
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        if stopEvent.is_set():
            rawCapture.truncate(0)
            return
        # convert img as Array
        image = frame.array
        # append label
        picname = "/home/pi/Documents/Patate/Pics/Auto/" + str(label) + "_" + str(time.time()) + ".jpg"
        cv2.imshow("Auto DataSet Mining", image)
        # take a pic
        #if label[0] != -1:
            #cv2.imwrite(picname, image)
        print("snap : " + picname)
        # Clean image before the next comes
        time.sleep(delay)
        rawCapture.truncate(0)


def controls(speed, direction):
    # Init engines
    POW.start(0)
    DIR.start(0)
    while True:
        # non blocking 'wait for key'
        key = cv2.waitKey(1) & 0xFF
        if key == ord('a'):
            print("Stop")
            stopEvent.set()
            return
        elif key == ord("z"):
            #if stopped, go
            if label[0] == -1:
                label[0] = 0
                speed = SPEED_NORMAL
                label[1] = 2
            #if turning, go forward
            elif label[0] == 0 and label[1] != 2:
                label[1] = 2
            #if forward, speed up
            elif label[0] == 0 and label[1] == 2:
                label[0] = 1
                speed = SPEED_FAST
        elif key == ord("q"):
            label[0] = 0
            speed = SPEED_NORMAL
            #go left
            if label[1] > 0:
                label[1] -= 1
        elif key == ord("s"):
            if label[0] == 0:
                label[0] = -1
                speed = 0
            elif label[0] == 1:
                label[0] = 0
                speed = SPEED_NORMAL
        elif key == ord("d"):
            label[0] = 0
            speed = SPEED_NORMAL
            #go right
            if label[1] < 4:
                label[1] += 1
                
        if label[1] == 0:
            direction = DIR_L_M
        elif label[1] == 1:
            direction = DIR_L
        elif label[1] == 2:
            direction = DIR_C
        elif label[1] == 3:
            direction = DIR_R
        elif label[1] == 4:
            direction = DIR_R_M
            
        POW.ChangeDutyCycle(speed)
        DIR.ChangeDutyCycle(direction)

video_thread = threading.Thread(target=videoLoop, args=(delay))
stopEvent = threading.Event()
if __name__ == "__main__":
    print("Press Ctrl+C to start/stop...")
    try:
      while True:
        pass
    except KeyboardInterrupt:
      pass
    
    print("Start video thread")
    try:
        video_thread.start()
        print("Ready to Go !")
        controls(speed, direction)
    except:
        pass
    cv2.destroyAllWindows()
    GPIO.cleanup()



