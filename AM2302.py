import adafruit_dht

dhtDevice = adafruit_dht.DHT22(board.D4)
#dht = adafruit_dht.DHT22(4)


t = dht.temperature
h = dht.humidity

print(t, h)
