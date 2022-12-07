from maplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import time

import board
import adafruit_dht

fig = plt.fiqure()
ax = plt.axes(xlim=(0, 50), ylim=(15, 45))
line, = ax.plot([], [], lw=1, c='yellow', marker='d', ms=2)
max_points = 50
line, = ax.plot(np.arange(max_points), np.ones(max_points, dtype=np.float)*np.nan, lw=1, c='yellow', marker='d', ms=2)

def init():
    return line

dhtDevice = adafruit_dht.DHT22(board.D24)

def get_y():
    h = dhtDevice.read_retry(dhtDevice.humidity)
    t = dhtDevice.read_retry(dhtDevice.temperature)
    return h

def animate(i):

    y = get_y()

    old_y = line.get_ydata()
    new_y = np.r_[old_y[1:], y]
    line.set_ydata(new_y)
    print(new_y)
    return line,

anim = animation.FuncAnimation(fig, animate, init_func=init, frames = 200, interval = 20, blit = false)
plt.show()
