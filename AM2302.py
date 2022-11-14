import adafruit_dht

dht_device = adafruit_dht.DHT22(23)

tem = dht_device.temperature
hum = dht_device.humidity

print(tem, hum)
