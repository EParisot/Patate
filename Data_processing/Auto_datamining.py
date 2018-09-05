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

SPEED_NORMAL = 6.76 # 6.8
SPEED_FAST = 6.6   # 6.65

DIR_L_M = 5
DIR_L = 6.5
DIR_C = 7
DIR_R = 7.5
DIR_R_M = 9

class Controler(object):
    def __init__(self):
        if len(sys.argv) == 2:
            self.delay = [float(sys.argv[1])]

        self.label = [-1, 2]

        #init GPIO with BCM numberings
        GPIO.setmode(GPIO.BCM)
        #init every used pins
        GPIO.setup(23, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)
        #set controls
        self.POW = GPIO.PWM(18, 50)
        self.DIR = GPIO.PWM(23, 50)

        # Init speed
        self.speed = SPEED_NORMAL

        # Init direction
        self.direction = DIR_C

        self.video_thread = threading.Thread(target=self.videoLoop, args=())
        self.stopEvent = threading.Event()

    # Loop over camera frames
    def videoLoop(self):
        # Setup Camera
        camera = PiCamera()
        camera.resolution = (160, 128)
        camera.framerate = 60
        camera.hflip = True
        camera.vflip = True
        rawCapture = PiRGBArray(camera, size = (160, 120))
        time.sleep(0.5)
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            if self.stopEvent.is_set():
                camera.close()
                cv2.destroyAllWindows()
                return
            time.sleep(self.delay[0])
            # convert img as Array
            image = frame.array
            # append label
            picname = "/home/pi/Documents/Patate/Pics/Auto/" + str(self.label[0]) + "_" + str(self.label[1]) + "_" + str(time.time()) + ".jpg"
            cv2.imshow("Auto DataSet Mining", image)
            # take a pic
            #if label[0] != -1:
                #cv2.imwrite(picname, image)
            print("snap : " + picname)
            # Clean image before the next comes
            #time.sleep(self.delay[0])
            rawCapture.truncate(0)

    def controls(self):
        # Init engines
        self.POW.start(0)
        self.DIR.start(0)
        while True:
            # non blocking 'wait for key'
            key = cv2.waitKey(1) & 0xFF
            if key == ord('a'):
                print("Stop")
                self.stopEvent.set()
                return
            elif key == ord("z"):
                #if stopped, go
                if self.label[0] == -1:
                    self.label[0] = 0
                    self.speed = SPEED_NORMAL
                    self.label[1] = 2
                #if turning, go forward
                elif self.label[0] == 0 and self.label[1] != 2:
                    self.label[1] = 2
                #if forward, speed up
                elif self.label[0] == 0 and self.label[1] == 2:
                    self.label[0] = 1
                    self.speed = SPEED_FAST
            elif key == ord("q"):
                self.label[0] = 0
                self.speed = SPEED_NORMAL
                #go left
                if self.label[1] > 0:
                    self.label[1] -= 1
            elif key == ord("s"):
                if self.label[0] == 0:
                    self.label[0] = -1
                    self.speed = 0
                elif self.label[0] == 1:
                    self.label[0] = 0
                    self.speed = SPEED_NORMAL
            elif key == ord("d"):
                self.label[0] = 0
                self.speed = SPEED_NORMAL
                #go right
                if self.label[1] < 4:
                    self.label[1] += 1
                    
            if self.label[1] == 0:
                self.direction = DIR_L_M
            elif self.label[1] == 1:
                self.direction = DIR_L
            elif self.label[1] == 2:
                self.direction = DIR_C
            elif self.label[1] == 3:
                self.direction = DIR_R
            elif self.label[1] == 4:
                self.direction = DIR_R_M
                
            self.POW.ChangeDutyCycle(self.speed)
            self.DIR.ChangeDutyCycle(self.direction)

if __name__ == "__main__":
    print("Press Ctrl+C to start/stop...")
    try:
      while True:
        pass
    except KeyboardInterrupt:
      pass
    
    controler = Controler()
    try:
        print("Starting video thread")
        controler.video_thread.start()
    except:
        print("Thread Error")
        GPIO.cleanup()
        exit(0)
    if controler.video_thread.is_alive() :
        print("Ready to Go !")
        controler.controls()
        controler.video_thread.join()
    else:
        print("Thread Error")
        
    GPIO.cleanup()



