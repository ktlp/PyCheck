#!/usr/bin/env python3

import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# plot style
plt.style.use('dark_background')

# starting data (tiime window length and initialization)
win_len = 120
win = deque([0] * win_len)
temp = np.diff(np.asarray(list(win)))

# declare  figure
fig, ax = plt.subplots()

# figure parameters
fig.dpi = 80
xlabel = "Time in secs"
ylabel = "~ kbytes deviation"
title = "Network Visualizer"
wtitle = "Bandwidth Plot"


# set parameters
fig.canvas.set_window_title(wtitle)
txt = plt.text(0.028, 0.896,'matplotlib', horizontalalignment='left', verticalalignment='bottom',
               transform=ax.transAxes, fontsize = 15, color='green', bbox = {'facecolor':'green','alpha':0.2, 'pad':10})
ymin, ymax = 0, max(temp)
plt.ylim(ymin,ymax)
plt.xticks(np.arange(0,130,10),reversed(np.arange(0,130,10)))
ax.set_title(title)
plt.ylabel(ylabel)
plt.xlabel(xlabel)
plt.grid()

# plot initial state
line, = ax.plot(temp)

# open /proc/net/dev file for network data
f = open("/proc/net/dev")

# update function for animation
def update(data):
    # differentiate data
    new_data = np.diff(data)

    # set new axis limits
    ymin, ymax = min(new_data), max(new_data)
    plt.ylim(ymin,ymax)

    # update plot & text
    line.set_ydata(new_data)
    s = "kbytes down: " + str(data[-1])
    txt.set_text(s)
    return line, txt,

# function to get data from file
def read_data():
    while True:
        # keep only wlan info
        for i,line in enumerate(f):
            if i == 3:
                x = int(float(line.split()[1])/1024) # to kilobytes
                # insert new measurement and pop oldest of the window
                win.append(x)
                win.popleft()
                temp = np.asarray(list(win))
                time.sleep(1)
        # return to the beggining of the file
        f.seek(0)
        yield temp

# animate
ani = animation.FuncAnimation(fig, update, read_data, interval = 100)
plt.show()