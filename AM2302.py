# sudo pip3 install Adafruit_DHT

import Adafruit_DHT as dht
import time

while True:
	humidity, temperature = dht.read_retry(dht.DHT22, 4)
	print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
	time.sleep(1)
