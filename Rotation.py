import RPi.GPIO as GPIO
import time, math

dist_meas = 0.00
km_per_hour = 0
rpm = 0
elapse = 0
pulse = 0
start_timer = time.time()

def init_GPIO():
    GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location
    GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)

def calc_elapsed(channel):
    global pulse, start_timer, elapse
    pulse += 1
    elapse = time.time() - start_timer
    start_timer = time.time()
    
def calc_speed(r_cm):
    global pulse, elapse, rpm, dist_km, dist_meas, km_per_sec, km_per_hour
    if elapse != 0:
        rpm = 1 / elapse * 60
        circ_cm = 34 #(2 * math.pi) * r_cm
        dist_km = circ_cm / 100000
        km_per_sec = dist_km / elapse
        km_per_hour = km_per_sec * 3600
        dist_meas = (dist_km * pulse) * 1000
        return km_per_hour

def init_interrupt():
    GPIO.add_event_detect(4, GPIO.FALLING, callback = calc_elapsed, bouncetime = 20)

if __name__ == '__main__':
    init_GPIO()
    init_interrupt()
    while True:
        calc_speed(20)
        print('rpm:{0:.0f}-RPM kmh:{1:.0f}-KMH dist_meas:{2:.0f}'.format(rpm, km_per_hour, dist_meas))
        time.sleep(0.1)