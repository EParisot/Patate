import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

#GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

#mot = GPIO.PWM(18, 50)
DIR = GPIO.PWM(23, 50)

#mot.start(0)
DIR.start(7)

#mot.ChangeDutyCycle(10)
#time.sleep(2)

DIR.ChangeDutyCycle(7)
time.sleep(2)
DIR.ChangeDutyCycle(4)
time.sleep(2)
DIR.ChangeDutyCycle(7)
time.sleep(2)
DIR.ChangeDutyCycle(10)
time.sleep(2)


#mot.stop()
GPIO.cleanup()
