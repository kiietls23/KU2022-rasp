from datetime import datetime, timedelta
import pprint
import time
from influxdb import InfluxDBClient
from copy import deepcopy

# 미세먼지센서
import serial
import struct

# 온습도센서
import board
import adafruit_dht

dhtDevice = adafruit_dht.DHT22(board.D24)
t = dhtDevice.temperature
h = dhtDevice.humidity

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


# influxdb에 연결하는 함수
def get_ifdb(db, host = 'localhost', port = 8086, user = 'root', passwd = 'root'):
    client = InfluxDBClient(host, port, user, passwd, db)

    try:
        client.create_database(db)

        print('Connection Successful')
        print('=========================')
        print('Connection Info')
        print('=========================')
        print('host:', host)
        print('username :', user)
        print('database :', db)

    except:
        print('Connection Failed')
        pass

    return client

# 연결된 데이터베이스에 데이터를 입력하는 함수
def my_test(ifdb):
    json_body = []
    tablename = 'sensor_data'
    fieldname = 'mydata'
    data = dust.unpack_data(buffer)
    point = {
        "measurement":tablename,
        "tags":{
            
        },
        "fields":{
            "PM 1.0": data[dust.DUST_PM1_0_CF1],
            "PM 2.5": data[dust.DUST_PM2_5_CF1],
            "PM 10.0": data[dust.DUST_PM10_0_CF1],
            "0.3um in 0.1L of air": data[dust.DUST_AIR_0_3],
            "0.5um in 0.1L of air": data[dust.DUST_AIR_0_5],
            "1.0um in 0.1L of air": data[dust.DUST_AIR_1_0],
            "2.5um in 0.1L of air": data[dust.DUST_AIR_2_5],
            "5.0um in 0.1L of air": data[dust.DUST_AIR_5_0],
            "10.0um in 0.1L of air": data[dust.DUST_AIR_10_0],
            "temperature": dhtDevice.temperature,
            "humidity": dhtDevice.humidity
        },
        "time":None,
    }

    vals = list(range(1,11))

    for v in vals:
        dt = datetime.now() - timedelta(hours=-9) # 한국 시간 UTC 9 고려

        np = deepcopy(point)
        np['fields'][fieldname] = v
        np['time'] = dt
        json_body.append(np)

        time.sleep(1)

    ifdb.write_points(json_body)

    result = ifdb.query('select * from %s'%tablename)
    pprint.pprint(result.raw)

def do_test(): # 코드 실행 시 가장 먼서 do_test 함수 실행
    mydb = get_ifdb(db='sensor_data')

    my_test(mydb)

if __name__ == '__main__':

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

    do_test()
