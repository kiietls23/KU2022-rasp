import adafruit_dht

dht_device = adafruit_dht.DHT22(D4)

tem = dht_device.temperature
hum = dht_device.humidity

print(tem, hum)
