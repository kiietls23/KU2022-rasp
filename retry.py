import board
import adafruit_dht

dht = adafruit_dht.DHT22(board.D4)

t = dht.temperature
h = dht.humidity

print(t, h)
