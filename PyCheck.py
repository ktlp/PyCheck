#!/usr/bin/env python3

import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
from matplotlib import style

#declare window

# show 60 secs before
win_len = 120

# list
win = deque([0] * win_len)
temp = np.asarray(list(win))

#DECLARE FIGURE
fig, ax = plt.subplots()
line, = ax.plot(temp)
ax.set_title('Time Elapsed')
fig.figsize = (3,8)
#OPEN FILE
f = open("/proc/net/dev")

def update(data):
    line.set_ydata(data)
    return line,

def read_data():
    while True:
        for i,line in enumerate(f):
            if i == 3:
                x = int(float(line.split()[1]))
                print(x)
                win.append(x)
                win.popleft()
                temp = np.asarray(list(win))
        f.seek(0)
        yield temp

ani = animation.FuncAnimation(fig, update, read_data, interval = 1000)
plt.show()