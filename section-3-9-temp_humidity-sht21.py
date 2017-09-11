import smbus
import time

SHT21_ADD = 0x40
SHT21_STATUS_MASK = 0xFFFC

SHT21_MEASURE_TEMP_CMD = 0xF3
SHT21_MEASURE_HUM_CMD = 0xF5

def get_temperature():
    bus.write_byte(SHT21_ADD, SHT21_MEASURE_TEMP_CMD)

    time.sleep(0.1)

    temp_msb = bus.read_byte (SHT21_ADD)
    temp_lsb = bus.read_byte (SHT21_ADD)
    temp_chksm = bus.read_byte (SHT21_ADD)
    
    temperature = (temp_msb << 8) + temp_lsb
    temperature &= SHT21_STATUS_MASK
    temperature *= 175.72
    temperature /= 1<<16
    temperature -= 46.85

    return temperature


def get_humidity():
    bus.write_byte(SHT21_ADD, SHT21_MEASURE_HUM_CMD)

    time.sleep(0.1)

    hum_msb = bus.read_byte (SHT21_ADD)
    hum_lsb = bus.read_byte (SHT21_ADD)
    hum_chksm = bus.read_byte (SHT21_ADD)

    humidity = (hum_msb << 8) + hum_lsb
    humidity &= SHT21_STATUS_MASK
    humidity *= 125.0
    humidity /= 1<<16
    humidity -= 6

    return humidity

try:
    bus = smbus.SMBus(1)

    print "Temperature is %s" % get_temperature()
    print "Humidity is %s" % get_humidity()
    
except:
    #print Error
    print "Error in executing I2C device program"
