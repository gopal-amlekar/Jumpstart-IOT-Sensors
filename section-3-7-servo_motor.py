import RPi.GPIO as GPIO
import time

servoPin = 23

GPIO.setmode(GPIO.BOARD)

GPIO.setup(servoPin, GPIO.OUT)

servoPWM = GPIO.PWM(servoPin, 50)

servoPWM.start(7.5)

try:
    while True:
        servoPWM.ChangeDutyCycle(7.5)  # turn towards 90 degree
        time.sleep(1) # sleep 1 second
        servoPWM.ChangeDutyCycle(2.5)  # turn towards 0 degree
        time.sleep(1) # sleep 1 second
        servoPWM.ChangeDutyCycle(12.5) # turn towards 180 degree
        time.sleep(1) # sleep 1 second 
        
except KeyboardInterrupt:
	servoPWM.stop()
	GPIO.cleanup()
