import RPi.GPIO as GPIO

#init GPIO with BCM numberings
GPIO.setmode(GPIO.BCM)

#init every used pins
GPIO.setup(12, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)

#set vars
MOT1v = GPIO.PWM(12, 50)
MOT1f = 19
MOT1b = 13
MOT2v = GPIO.PWM(16, 50)
MOT2f = 21
MOT2b = 20
speed = 0.5

def Forward(speed):
  GPIO.output(MOT1b, LOW)
  GPIO.output(MOT2b, LOW)
  GPIO.output(MOT1f, HIGH)
  GPIO.output(MOT2f, HIGH)
  MOT1v.start(speed)
  MOT2v.start(speed)
  
def Brake(speed):
  MOT1v.ChangeFrequency(speed - 0.2)
  MOT2v.ChangeFrequency(speed - 0.2)

def Stop():
  MOT1v.ChangeFrequency(0)
  MOT2v.ChangeFrequency(0)
  MOT1v.stop()
  MOT2v.stop()
  
def TurnR(speed):
  MOT1v.ChangeFrequency(speed - 0.1)
  MOT2v.ChangeFrequency(speed + 0.2)
  
def TurnL(speed):
  MOT1v.ChangeFrequency(speed + 0.2)
  MOT2v.ChangeFrequency(speed - 0.1)


#Video here

#IA here





GPIO.cleanup()
