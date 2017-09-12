import RPi.GPIO as GPIO
import numpy as np
import time


STEP_PIN = 7
DIR_PIN = 8
M1_PIN = 9
M0_PIN = 10

NSLEEP_PIN = 11
NFAULT_PIN = 14
NENBL_PIN = 15
CONFIG_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

steps = 20
micro_step = 1.0 / 4 #Possible values: 1.0, 1.0/2, 1.0/4, 1.0/8, 1.0/16, 1.0/32

print "Motor rotation by %g steps " % (steps / micro_step)

GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(NSLEEP_PIN, GPIO.OUT)
GPIO.setup(NFAULT_PIN, GPIO.IN)
GPIO.setup(NENBL_PIN, GPIO.OUT)
GPIO.setup(CONFIG_PIN, GPIO.OUT)


GPIO.output(NSLEEP_PIN, False)  #Low power and reset all logic
GPIO.output(CONFIG_PIN, True)   #Indexer mode
GPIO.output(NSLEEP_PIN, True)   #Enable device

time.sleep(0.001)

while GPIO.input(NFAULT_PIN)==0:
	time.sleep(0.001)

GPIO.output(NENBL_PIN, False) #Enable all outputs

if steps < 0:
    GPIO.output(DIR_PIN, False) #Anticlockwise
    steps = -steps
else:
    GPIO.output(DIR_PIN, True)  #Clockwise

# Set the mode pins M0 and M1 to appropriate state
# Setting a pin as input puts it in high impedance mode

if micro_step == 1:
    GPIO.setup(M1_PIN, GPIO.OUT)
    GPIO.output(M1_PIN, False)
    GPIO.setup(M0_PIN, GPIO.OUT)
    GPIO.output(M0_PIN, False)
elif micro_step == 1.0/2:
    GPIO.setup(M1_PIN, GPIO.OUT)
    GPIO.output(M1_PIN, False)
    GPIO.setup(M0_PIN, GPIO.OUT)
    GPIO.output(M0_PIN, True)
elif micro_step == 1.0/4:
    GPIO.setup(M1_PIN, GPIO.OUT)
    GPIO.output(M1_PIN, False)
    GPIO.setup(M0_PIN, GPIO.IN)
elif micro_step == 1.0/8:
    GPIO.setup(M1_PIN, GPIO.OUT)
    GPIO.output(M1_PIN, True)
    GPIO.setup(M0_PIN, GPIO.OUT)
    GPIO.output(M0_PIN, False)
elif micro_step == 1.0/16:
    GPIO.setup(M1_PIN, GPIO.OUT)
    GPIO.output(M1_PIN, True)
    GPIO.setup(M0_PIN, GPIO.OUT)
    GPIO.output(M0_PIN, True)
elif micro_step == 1.0/32:
    GPIO.setup(M1_PIN, GPIO.OUT)
    GPIO.output(M1_PIN, True)
    GPIO.setup(M0_PIN, GPIO.IN)

# Generate an array and use the count of the array only

for count in np.arange(0, steps, micro_step):
    time.sleep(0.05)
    GPIO.output(STEP_PIN, True) # High going pulse moves the motor
    time.sleep(0.05)
    GPIO.output(STEP_PIN, False)
    sys.stdout.write(".")
    sys.stdout.flush()

print "\nDone"
GPIO.cleanup()
