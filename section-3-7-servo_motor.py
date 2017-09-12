import RPi.GPIO as GPIO
import time

servoPin = 23

GPIO.setmode(GPIO.BCM)

GPIO.setup(servoPin, GPIO.OUT)

# Configure PWM to generate 50Hz (A pulse every 20msec) frequency
# Returns an object. Call various methods on the object
servoPWM = GPIO.PWM(servoPin, 50)


# Duty cycle = (ON time / Total time) * 100
# For 0 degrees: (0.5 / 20) * 100 = 2.5
# For 90 degrees:(1.5 / 20) * 100 = 7.5
# For 180 degrees:(2.5 / 20) * 100 = 12.5
# For any other angle, calculate accordingly using the formula above

# Start PWM with duty cycle 7.5% (Initial default 90 degrees)
servoPWM.start(7.5)

try:
    # Keep moving in 180 degree span from 0 to 90 to 180
    while True:
        servoPWM.ChangeDutyCycle(7.5)  # turn towards 90 degree
        time.sleep(1) # sleep 1 second
        servoPWM.ChangeDutyCycle(2.5)  # turn towards 0 degree
        time.sleep(1) # sleep 1 second
        servoPWM.ChangeDutyCycle(12.5) # turn towards 180 degree
        time.sleep(1) # sleep 1 second

except KeyboardInterrupt:
    # Must stop the PWM before exiting
	servoPWM.stop()
	GPIO.cleanup()
