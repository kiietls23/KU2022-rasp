from datetime import datetime, timedelta
import pprint
import time
from influxdb import InfluxDBClient
from copy import deepcopy

# 온습도센서
import board
import adafruit_dht

dhtDevice = adafruit_dht.DHT22(board.D24)
t = dhtDevice.temperature
h = dhtDevice.humidity

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
    tablename = 'my_table'
    fieldname = 'my_field'
    point = {
        "measurement":tablename,
        "tags":{
            "temperature": dhtDevice.temperature,
            "humidity": dhtDevice.humidity
        },
        "fields":{
            fieldname: 0
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
    mydb = get_ifdb(db='DHT22_DB')

    my_test(mydb)

if __name__ == '__main__':
    do_test()
