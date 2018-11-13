import Adafruit_PCA9685
import time

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

UP = 150
DOWN = 120

time.sleep(1)
pwm.set_pwm(2, 0, UP)
time.sleep(3)
pwm.set_pwm(2, 0, DOWN)
time.sleep(1)
pwm.set_pwm(2, 0, 0)
