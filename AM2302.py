import adafruit_dht
import board

dhtDevice = adafruit_dht.DHT22(board.D4)
#dht = adafruit_dht.DHT22(4)


t = dhtDevice.temperature
h = dhtDevice.humidity

print(t, h)
