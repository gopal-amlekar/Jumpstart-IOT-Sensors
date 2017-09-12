import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

# If running this code on IOTIFY,change TRIG to 5 and ECHO to 6
TRIG = 2
ECHO = 3

print "Distance Measurement In Progress"

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

# Stop transmission already going on, if any
GPIO.output(TRIG, False)
print "Waiting For Sensor To Settle"
time.sleep(2)

# 10 usec high-going pulse on trigger pin
GPIO.output(TRIG, True)
time.sleep(0.00001)
GPIO.output(TRIG, False)

# Wait till echo pin goes high
while GPIO.input(ECHO)==0:
    pulse_start = time.time()

# Now wait for the high period to be over i.e. till echo pin goes low
while GPIO.input(ECHO)==1:
    pulse_end = time.time()

# Pulse width in seconds
pulse_duration = pulse_end - pulse_start

# Consider velocity 343m/sec
# Distance = velocity * time
# Time measured here is two way - Transmit and recieve
# So Distance = velocity * (Time /2)
# With the velocity in cm, the formula becomes
# Distance = 34300 * (time / 2) = 17150 * time
distance = pulse_duration * 17150

distance = round(distance, 2)

print "Distance:",distance,"cm"

GPIO.cleanup()
