# calculates the visibility in a specific time period
# and puts it in a .csv
# Author: Tobias Neumann | RX23 Daedalus

import sys
from pyorbital import tlefile as tf
from pyorbital.orbital import Orbital as Orb
from datetime import datetime as dt
from datetime import timedelta as td

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pytz

# testing library
# tle_data = tf.read('Noaa 15')
# print(tle_data)
# quit()

# receiver position
lat = 48.02708
lon = 16.26235
alt = 0.1  # above sea level (Geoid) [km]
# lat = 48.27027
# lon = 14.4077
# alt = 0.25  # above sea level (Geoid) [km]
#  The minimum elevation angle for an earth station is 8.2 degrees. 
# http://www.kt.agh.edu.pl/~kulakowski/satelity/Iridium-Leo.pdf
# lets be more conservative with 10deg
elBound = 10.0  # limit for lowest elevation [deg]

# time settings
startTime = dt(year=2023, month=9, day=11, hour=19, tzinfo=pytz.utc)
hoursForecast = 2
arg1 = 0
resolution = 10  # [seconds]
# time zero
zero_time = dt(year=startTime.year, month=startTime.month, day=startTime.day, hour=0, tzinfo=startTime.tzinfo)

# input file settings (use spares[] to exclude spare Iridium satellites)
tleFile = 'iridium-NEXT.txt'
csvFile = 'satVis_' + str(startTime.day).zfill(2) + '-' + str(startTime.month).zfill(2) + '-' + str(
    startTime.year) + '-' + str(startTime.hour).zfill(2) + str(startTime.minute).zfill(2) +  '_' + str(hoursForecast) + 'hours'

# spares = ["IRIDIUM 124", "IRIDIUM 115", "IRIDIUM 175", "IRIDIUM 176", "IRIDIUM 170", "IRIDIUM 162", "IRIDIUM 161"]
# From https://en.wikipedia.org/wiki/Iridium_satellite_constellation#In-orbit_spares
# Spare satellites are usually held in a 666 kilometres (414 mi) storage orbit.
# 2023 May:    https://celestrak.org/NORAD/elements/table.php?GROUP=iridium-NEXT&FORMAT=tle
# 2023 May:    https://iridiumwhere.com/status/
#               Spares orbit at a lower altitude (750-770km). They also mark 105 as spare, which seems to be close to 164
#           http://www.rod.sladen.org.uk/iridium.htm
spares = ["IRIDIUM 124", "IRIDIUM 115", "IRIDIUM 175", "IRIDIUM 176", "IRIDIUM 170", "IRIDIUM 162", "IRIDIUM 161", "IRIDIUM 169"]

# variable initializations
currentTime = dt.utcnow()  # + td(seconds = 600)
currentTime = currentTime.replace(tzinfo=pytz.utc)
endTime = startTime + td(hours=hoursForecast)
timestep = td(seconds=resolution)
steps = (endTime - startTime).total_seconds() / resolution
satList = []
name = tle1 = tle2 = ''
with open(tleFile, 'rb') as f:
    for line in f:
        name = line.decode('utf-8')
        tle1 = next(f).decode('utf-8')
        tle2 = next(f).decode('utf-8')
        satList.append(Orb(satellite=name, line1=tle1, line2=tle2))

# print current visibility
print("\nsatellites visible right now (Current Time:", currentTime, ")")
for sat in satList:
    (az, el) = sat.get_observer_look(currentTime, lon, lat, alt)
    if el >= elBound:
        print(sat.satellite_name.rstrip(), end='')
        if sat.satellite_name.rstrip() in str(spares):
            print(" (spare)", end='')
        print()
print()

print("Generating", csvFile, "...\n")
csv = open(csvFile + '.csv', 'w')
csv.write('"minutes of the day","Sat visible Count"\r\n')  # table header
tempTime = startTime
timeVec = []
satCountVec = []
cnt = 0
print("|0%         .           |50%        .        100%|")
while tempTime < endTime:
    satCount = 0
    for sat in satList:
        (az, el) = sat.get_observer_look(tempTime, lon, lat, alt)
        if el >= elBound and not sat.satellite_name.rstrip() in str(spares):
            satCount += 1
    csv.write(str((tempTime - startTime).total_seconds() / 60) + ',' + str(satCount) + '\r\n')
    tempTime += timestep
    timeVec.append((tempTime-zero_time).total_seconds() / 60 / 60)
    satCountVec.append(satCount)
    # progress bar
    if cnt >= steps / 50:
        print('#', end='', flush=True)
        cnt -= steps / 50
    cnt += 1
print("#\ndone!")
csv.close()


# Convert array of integers to pandas series
numbers_series = pd.Series(satCountVec)
  
# Get the window of series
# of observations of specified window size
window_size = np.round(60/resolution)*10 
windows = numbers_series.rolling(int(window_size), center=True)
  
# Create a series of moving
# averages of each window
moving_averages = windows.mean()
  
# Convert pandas series back to list
satCountVec_moving_averages = moving_averages.tolist()

# plot a summary
y_max = max(satCountVec);
fig, ax = plt.subplots()
plt.title(str(startTime.day).zfill(2) + '-' + str(startTime.month).zfill(2) + '-' + str(
    startTime.year))
ax.step(timeVec, satCountVec, label='satellites')
ax.plot(timeVec, satCountVec_moving_averages, '--', label='Average')
ax.legend()
ax.set_ylabel(f'Number of satellites above {elBound} deg')
ax.set_xlabel('h in UTC')
ax.set(ylim=(0, y_max+1), yticks=np.arange(1, y_max+1))
plt.savefig(csvFile + '.png')
plt.show()