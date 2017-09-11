# Python code to read luminosity values from APDS-9301

import smbus
import time
import math

APDS93_ADDR = 0x29

def calc_lux(ch0, ch1):
    
    if ch0 == 0:
    	return None
    
    #Calculation based on datasheet. High gain used, scaling 1 (default)
    
    ch0 = float(ch0)
    ch1 = float(ch1)
    
    lux = 0
    
    d = ch1 / ch0
    if ch1 == ch0 == 65535:
    	return float('nan') # out of range
    if d > 0 and d <= 0.5:
    	lux = 0.0304 * ch0 - 0.062 * ch0 * math.pow(d, 1.4)
    elif d > 0.5 and d <= 0.61:
    	lux = 0.0224 * ch0 - 0.031 * ch1
    elif d > 0.61 and d <= 0.80:
    	lux = 0.0128 * ch0 - 0.0153 * ch1
    elif d > 0.80 and d <= 1.30:
    	lux = 0.00146 * ch0 - 0.00112 * ch1
    elif d > 1.3:
    	lux = 0
    
    return lux


    
try:
    bus = smbus.SMBus(1)
    
    #Set Power ON (Write 03h to control register (address 0x00)
    bus.write_byte_data(APDS93_ADDR, 0x80, 0x03)
    #Set high gain and integration time 402ms, scale 1
    bus.write_byte_data(APDS93_ADDR, 0x81, 0x12)
    
    while 1:
    # Read Channel 0 high and low byte in single cycle (Read word)
        ch0 = bus.read_word_data(APDS93_ADDR, 0xAC)
    
    # Read Channel 1 high and low byte in single cycle (Read word)
        ch1 = bus.read_word_data(APDS93_ADDR, 0xAE)
    
        print "Lux value is %s" % calc_lux(ch0, ch1)
        
        time.sleep(2)    
        
except IOError, e:
	print e
	print "Error creating connection to i2c.  Try running as root"
except KeyboardInterrupt:
    print "\nExiting"
