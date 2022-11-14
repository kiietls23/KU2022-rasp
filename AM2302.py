import adafruit_dht
import board

#dht_device = adafruit_dht.DHT22(4)
dht = adafruit_dht.DHT22(board.D4)


tem = dht.temperature
hum = dht.humidity

print(tem, hum)
