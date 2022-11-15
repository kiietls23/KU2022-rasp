import adafruit_dht

#dht_device = adafruit_dht.DHT22(4)
dht = adafruit_dht.DHT22(D4)


tem = dht.temperature
hum = dht.humidity

print(tem, hum)
