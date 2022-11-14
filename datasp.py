"""
# unpack_data(buffer)
# data list
HEADER_HIGH            = 0x42
HEADER_LOW             = 0x4d
FRAME_LENGTH           = 2x13+2(data+check bytes) 
DUST_PM1_0_CF1         = PM1.0 concentration unit μ g/m3（CF=1，standard particle）
DUST_PM2_5_CF1         = PM2.5 concentration unit μ g/m3（CF=1，standard particle）
DUST_PM10_0_CF1        = PM10 concentration unit μ g/m3（CF=1，standard particle）
DUST_PM1_0_ATM         = PM1.0 concentration unit μ g/m3（under atmospheric environment）
DUST_PM2_5_ATM         = PM2.5 concentration unit μ g/m3（under atmospheric environment）
DUST_PM10_0_ATM        = PM10 concentration unit μ g/m3  (under atmospheric environment) 
DUST_AIR_0_3           = indicates the number of particles with diameter beyond 0.3 um in 0.1 L of air. 
DUST_AIR_0_5           = indicates the number of particles with diameter beyond 0.5 um in 0.1 L of air. 
DUST_AIR_1_0           = indicates the number of particles with diameter beyond 1.0 um in 0.1 L of air. 
DUST_AIR_2_5           = indicates the number of particles with diameter beyond 2.5 um in 0.1 L of air. 
DUST_AIR_5_0           = indicates the number of particles with diameter beyond 5.0 um in 0.1 L of air. 
DUST_AIR_10_0          = indicates the number of particles with diameter beyond 10 um in 0.1 L of air. 
RESERVEDF              = Data13 Reserved high 8 bits
RESERVEDB              = Data13 Reserved low 8 bits
CHECKSUM               = Checksum code
# CF=1 should be used in the factory environment
"""

import serial
import struct
import time


class PMS7003(object):

    # PMS7003 protocol data (HEADER 2byte + 30byte)
    PMS_7003_PROTOCOL_SIZE = 32

    # PMS7003 data list
    HEADER_HIGH            = 0  # 0x42
    HEADER_LOW             = 1  # 0x4d
    FRAME_LENGTH           = 2  # 2x13+2(data+check bytes) 
    DUST_PM1_0_CF1         = 3  # PM1.0 concentration unit μ g/m3（CF=1，standard particle）
    DUST_PM2_5_CF1         = 4  # PM2.5 concentration unit μ g/m3（CF=1，standard particle）
    DUST_PM10_0_CF1        = 5  # PM10 concentration unit μ g/m3（CF=1，standard particle）
    DUST_PM1_0_ATM         = 6  # PM1.0 concentration unit μ g/m3（under atmospheric environment）
    DUST_PM2_5_ATM         = 7  # PM2.5 concentration unit μ g/m3（under atmospheric environment）
    DUST_PM10_0_ATM        = 8  # PM10 concentration unit μ g/m3  (under atmospheric environment) 
    DUST_AIR_0_3           = 9  # indicates the number of particles with diameter beyond 0.3 um in 0.1 L of air. 
    DUST_AIR_0_5           = 10 # indicates the number of particles with diameter beyond 0.5 um in 0.1 L of air. 
    DUST_AIR_1_0           = 11 # indicates the number of particles with diameter beyond 1.0 um in 0.1 L of air. 
    DUST_AIR_2_5           = 12 # indicates the number of particles with diameter beyond 2.5 um in 0.1 L of air. 
    DUST_AIR_5_0           = 13 # indicates the number of particles with diameter beyond 5.0 um in 0.1 L of air. 
    DUST_AIR_10_0          = 14 # indicates the number of particles with diameter beyond 10 um in 0.1 L of air. 
    RESERVEDF              = 15 # Data13 Reserved high 8 bits
    RESERVEDB              = 16 # Data13 Reserved low 8 bits
    CHECKSUM               = 17 # Checksum code


dust = PMS7003()

# Baud Rate
Speed = 9600

# UART / USB Serial
USB0 = '/dev/ttyUSB0'
UART = '/dev/ttyAMA0'

# USE PORT
SERIAL_PORT = UART
 
#serial setting
ser = serial.Serial(SERIAL_PORT, Speed, timeout = 1)


buffer = ser.read(1024)

#if(dust.protocol_chk(buffer)):
data = dust.unpack_data(buffer)

print ("PMS 7003 dust data")
print ("PM 1.0 : %s" % (data[dust.DUST_PM1_0_ATM]))
print ("PM 2.5 : %s" % (data[dust.DUST_PM2_5_ATM]))
print ("PM 10.0 : %s" % (data[dust.DUST_PM10_0_ATM]))

#else:
    #print ("data read Err")

ser.close()
