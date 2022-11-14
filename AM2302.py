import adafruit_dht

dht_device = adafruit_dht.DHT22(18)

tem = dht_device.temperature
hum = dht_device.humidity

print(tem, hum)
