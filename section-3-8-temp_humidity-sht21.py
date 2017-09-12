import smbus    # For handling I2C devices
import time

# Datasheet says 0x80 but IOTIFY has this on 0x40
# So if using on Raspberry Pi, change this to 0x80
SHT21_ADD = 0x40

# Both commands as specified in datasheet with no hold master mode
# No hold master mode allows I2C bus to be used by other devices if required
# We just insert some delay for the measurements to finish
SHT21_MEASURE_TEMP_CMD = 0xF3
SHT21_MEASURE_HUM_CMD = 0xF5

# Lower two bits need to be masked because
# LSB is not used and the next bit indicates measurement type i.e.
# temperature or humidiy. But we already know it. So ignore those 2 bits
SHT21_STATUS_MASK = 0xFFFC


# Function to measure and read raw temperature, convert it to temperature value as per datasheet
# The flow in Non hold master mode is:
# 1. Send Temperature measurement command
# 2. Wait for some time to finish the conversion
# 3. Read 3 bytes from the device
# 4. First 2 bytes give the temperature data and the 3rd one is checksum
# 5. Refer datasheet for checksum details
# 6. Convert the raw data in 1st 2 bytes (again as per datasheet) to temperature
def get_temperature():
    bus.write_byte(SHT21_ADD, SHT21_MEASURE_TEMP_CMD)

    time.sleep(0.1)

    temp_msb = bus.read_byte (SHT21_ADD)
    temp_lsb = bus.read_byte (SHT21_ADD)

    # Checksum is not used for now
    temp_chksm = bus.read_byte (SHT21_ADD)

    # Following code for converting raw data to actual temperature value
    # Calculations Based on datasheet
    temperature = (temp_msb << 8) + temp_lsb
    temperature &= SHT21_STATUS_MASK
    temperature *= 175.72
    temperature /= 1<<16
    temperature -= 46.85

    return temperature


# Function to measure and read raw humidity, convert it to humidity value as per datasheet
# The flow in Non hold master mode is:
# 1. Send Humidity measurement command
# 2. Wait for some time to finish the conversion
# 3. Read 3 bytes from the device
# 4. First 2 bytes give the humidity data and the 3rd one is checksum
# 5. Refer datasheet for checksum details
# 6. Convert the raw data in 1st 2 bytes (again as per datasheet) to humidity
def get_humidity():
    bus.write_byte(SHT21_ADD, SHT21_MEASURE_HUM_CMD)

    time.sleep(0.1)

    hum_msb = bus.read_byte (SHT21_ADD)
    hum_lsb = bus.read_byte (SHT21_ADD)

    # Checksum is not used for now
    hum_chksm = bus.read_byte (SHT21_ADD)

    # Following code for converting raw data to actual humidity value
    # Calculations Based on datasheet
    humidity = (hum_msb << 8) + hum_lsb
    humidity &= SHT21_STATUS_MASK
    humidity *= 125.0
    humidity /= 1<<16
    humidity -= 6

    return humidity

# Main code execution starts here
try:
    # Use I2C device 1. Earlier old Raspberry Pi have device at 0
    # This is the I2C controller device on the Pi, not to be confused with
    # the I2C device we are controlling (for e.g. SHT21)
    bus = smbus.SMBus(1)

    print "Temperature is %s" % get_temperature()
    print "Humidity is %s" % get_humidity()

except:
    #print Error
    # Generic error
    print "Error in executing I2C device program"
