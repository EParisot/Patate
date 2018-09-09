# Import the PCA9685 module.
import Adafruit_PCA9685

# import xbox driver
import xbox

import time
from picamera import PiCamera
from picamera.array import PiRGBArray
from PIL import Image
import sys
import threading

#############################################

SPEED_NORMAL = 320#6.8 # 6.8
SPEED_FAST = 315#6.65   # 6.65

DIR_L_M = 245
DIR_L = 307
DIR_C = 328
DIR_R = 348
DIR_R_M = 409

class Controler(object):
    def __init__(self):
        self.snap = False
        if len(sys.argv) == 2:
            self.delay = float(sys.argv[1])
            self.snap = True
        else:
            print("No Snaps, specify a delay value (float) to activate")

        self.label = [-1, 2]

        #set controls
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)

        # Init speed
        self.speed = SPEED_NORMAL
        # Init direction
        self.direction = DIR_C
        
        # Setup Camera
        self.camera = PiCamera()
        self.camera.resolution = (160, 96)
        self.camera.framerate = 30
        #self.camera.hflip = True
        #self.camera.vflip = True
        self.rawCapture = PiRGBArray(self.camera, size = (160, 96))
        time.sleep(0.5)
        
        self.joy = xbox.Joystick()
        

    # Loop over camera frames
    def videoLoop(self):
        start = time.time()
        i = 0
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            # convert img as Array
            image = frame.array
            # append label
            picname = "/home/pi/Documents/Patate/Pics/Auto/" + str(self.label[0]) + "_" + str(self.label[1]) + "_" + str(time.time()) + ".jpg"
            #cv2.imshow("Auto DataSet Mining", image)
            # take a pic
            if self.label[0] != -1 and self.snap == True:
                if time.time() - start > self.delay:
                    #cv2.imwrite(picname, image)
                    im = Image.fromarray(image)
                    im.save(picname)
                    if self.label[1] != 2 :
                        if self.label[1] == 0:
                            rev_label = 4
                        elif self.label[1] == 1 :
                            rev_label = 3
                        elif self.label[1] == 3:
                            rev_label = 1
                        elif self.label[1] == 4 :
                            rev_label = 0
                        picname = "/home/pi/Documents/Patate/Pics/Auto/" + str(self.label[0]) + "_" + str(rev_label) + "_r" + str(time.time()) + ".jpg"
                        im = im.transpose(Image.FLIP_LEFT_RIGHT)
                        im.save(picname)
                        i += 1
                    start = time.time()
                    print(str(i) + " - snap : " + picname)
                    i += 1
            # Clean image before the next comes
            self.rawCapture.truncate(0)
            
            # non blocking 'wait for key'
            if self.joy.A():                   #Test state of the A button (1=pressed, 0=not pressed)
                self.pwm.set_pwm(0, 0, 0)
                self.pwm.set_pwm(1, 0, 0)
                print("Stop")
                return
            self.controls()

    def controls(self):
        
        trigger  = self.joy.rightTrigger() #Right trigger position (values 0 to 1.0)
        if trigger > 0:
            if trigger < 0.6:
                self.label[0] = 0
                self.speed = SPEED_NORMAL
            else:
                self.label[0] = 1
                self.speed = SPEED_FAST
        else:
            self.label[0] = -1
            self.speed = 0
            
        cur_x = self.joy.leftX()      #X-axis of the left stick (values -1.0 to 1.0)
        if cur_x < -0.1:
            if cur_x < -0.6:
                self.label[1] = 0
                self.direction = DIR_L_M
            else:
                self.label[1] = 1
                self.direction = DIR_L
        elif cur_x > 0.1:
            if cur_x > 0.6:
                self.label[1] = 4
                self.direction = DIR_R_M
            else:
                self.label[1] = 3
                self.direction = DIR_R
        else:
            self.label[1] = 2
            self.direction = DIR_C
                        
        self.pwm.set_pwm(0, 0, self.direction)
        self.pwm.set_pwm(1, 0, self.speed)

if __name__ == "__main__":
    print("Press Ctrl+C to start/stop...")
    try:
      while True:
        pass
    except KeyboardInterrupt:
      pass
    controler = Controler()
    controler.videoLoop()
    controler.joy.close()
    controler.camera.close()
    
    



