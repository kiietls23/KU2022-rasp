import adafruit_dht
import board

#dht_device = adafruit_dht.DHT22(4)
dht = adafruit_dht.DHT22(board.D4)


tem = dht_device.temperature
hum = dht_device.humidity

print(tem, hum)
