# PMS7003
import serial
import struct
import time

#DHT22
import board
import adafruit_dht

# AirKorea OpenAPI 사용
import requests
from bs4 import BeautifulSoup
import pandas
import urllib3 # 경고 무시

urllib3.disable_warnings()

M = '&numOfRows=1&pageNo=1&stationName=신흥동&dataTerm=DAILY&ver=1.3'
key ='tsFgvelgFo8g9a12hc4f1YCn9z2S16kGxMe7FbBTAaPyEcR8gI2K8bFpegdO2S4ngadYMTWn64d0MFzYHzH71w%3D%3D'
url ='https://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?serviceKey=' + key + M

# requests CERTIFICATE_VERIFY_FAILED 경고 무시
session = requests.Session()
session.verify = False
session.post(url='https://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?serviceKey=' + key + M, data={'bar':'baz'})

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
ItemList = soup.findAll('item')
for item in ItemList:
    a = item.find('datatime').text
    g = item.find('pm10value').text
    i = item.find('pm25value').text
    s = item.find('pm10grade1h').text
    t = item.find('pm25grade1h').text
    print('측정소: 신흥동')
    print('측정시간:' + a)
    print('미세먼지 농도:' + g + '㎍/㎥<'+ s +'>')
    print('초미세먼지 농도:' + i + '㎍/㎥<'+ s +'>')
    print('좋음 1 | 보통 2 | 나쁨 3 | 매우나쁨 4')


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


    # header check
    def header_chk(self, buffer):

        if (buffer[self.HEADER_HIGH] == 66 and buffer[self.HEADER_LOW] == 77):
            return True

        else:
            return False

    # chksum value calculation
    def chksum_cal(self, buffer):

        buffer = buffer[0:self.PMS_7003_PROTOCOL_SIZE]

        # data unpack (Byte -> Tuple (30 x unsigned char <B> + unsigned short <H>))
        chksum_data = struct.unpack('!30BH', buffer)

        chksum = 0

        for i in range(30):
            chksum = chksum + chksum_data[i]

        return chksum

    # checksum check
    def chksum_chk(self, buffer):

        chk_result = self.chksum_cal(buffer)

        chksum_buffer = buffer[30:self.PMS_7003_PROTOCOL_SIZE]
        chksum = struct.unpack('!H', chksum_buffer)

        if (chk_result == chksum[0]):
            return True

        else:
            return False

    # protocol size(small) check
    def protocol_size_chk(self, buffer):

        if(self.PMS_7003_PROTOCOL_SIZE <= len(buffer)):
            return True

        else:
            return False

    # protocol check
    def protocol_chk(self, buffer):

        if(self.protocol_size_chk(buffer)):

            if(self.header_chk(buffer)):

                if(self.chksum_chk(buffer)):

                    return True
                else:
                    print("Chksum err")
            else:
                print("Header err")
        else:
            print("Protol err")

        return False

    # unpack data
    # <Tuple (13 x unsigned short <H> + 2 x unsigned char <B> + unsigned short <H>)>
    def unpack_data(self, buffer):

        buffer = buffer[0:self.PMS_7003_PROTOCOL_SIZE]

        # data unpack (Byte -> Tuple (13 x unsigned short <H> + 2 x unsigned char <B> + unsigned short <H>))
        data = struct.unpack('!2B13H2BH', buffer)

        return data


    def print_serial(self, buffer):

        chksum = self.chksum_cal(buffer)
        data = self.unpack_data(buffer)

        print ("============================================================================")
        print ("Header : %c %c \t\t | Frame length : %s" % (data[self.HEADER_HIGH], data[self.HEADER_LOW], data[self.FRAME_LENGTH]))
        print ("PM 1.0 (CF=1) : %s\t | PM 1.0 : %s" % (data[self.DUST_PM1_0_CF1], data[self.DUST_PM1_0_ATM]))
        print ("PM 2.5 (CF=1) : %s\t | PM 2.5 : %s" % (data[self.DUST_PM2_5_CF1], data[self.DUST_PM2_5_ATM]))
        print ("PM 10.0 (CF=1) : %s\t | PM 10.0 : %s" % (data[self.DUST_PM10_0_CF1], data[self.DUST_PM10_0_ATM]))
        print ("0.3um in 0.1L of air : %s" % (data[self.DUST_AIR_0_3]))
        print ("0.5um in 0.1L of air : %s" % (data[self.DUST_AIR_0_5]))
        print ("1.0um in 0.1L of air : %s" % (data[self.DUST_AIR_1_0]))
        print ("2.5um in 0.1L of air : %s" % (data[self.DUST_AIR_2_5]))
        print ("5.0um in 0.1L of air : %s" % (data[self.DUST_AIR_5_0]))
        print ("10.0um in 0.1L of air : %s" % (data[self.DUST_AIR_10_0]))
        print ("Reserved F : %s | Reserved B : %s" % (data[self.RESERVEDF],data[self.RESERVEDB]))
        print ("CHKSUM : %s | read CHKSUM : %s | CHKSUM result : %s" % (chksum, data[self.CHECKSUM], chksum == data[self.CHECKSUM]))
        print ("============================================================================")



# UART / USB Serial : 'dmesg | grep ttyUSB'
USB0 = '/dev/ttyUSB0'
UART = '/dev/ttyAMA0'

# USE PORT
SERIAL_PORT = UART

# Baud Rate
Speed = 9600

print(time.strftime('%Y-%m-%d %H:%M:%S'))

# example
"""
if __name__=='__main__':
    #serial setting
    ser = serial.Serial(SERIAL_PORT, Speed, timeout = 5)
    dust = PMS7003()
    while True:
        ser.flushInput()
        buffer = ser.read(1024)
        if(dust.protocol_chk(buffer)):
            print("DATA read success")
            # print data
            dust.print_serial(buffer)
        else:
            print("DATA read fail...")
    ser.close()
"""

ser = serial.Serial(SERIAL_PORT, Speed, timeout = 5)

dust = PMS7003()

ser.flushInput()
buffer = ser.read(1024)

if(dust.protocol_chk(buffer)):

    print("DATA read success")

    # print data
    dust.print_serial(buffer)

else:

    print("DATA read fail...")

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D24)

temperature_c = dhtDevice.temperature
temperature_f = temperature_c * (9 / 5) + 32
humidity = dhtDevice.humidity
print("temperature: {:.1f} F / {:.1f} C       humidity: {}%".format(temperature_f, temperature_c, humidity))
