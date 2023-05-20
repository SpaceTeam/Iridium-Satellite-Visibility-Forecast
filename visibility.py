# calculates the visibility in a specific time period
# and puts it in a .csv
# Author: Tobias Neumann | RX23 Daedalus

import sys
from pyorbital import tlefile as tf
from pyorbital.orbital import Orbital as Orb
from datetime import datetime as dt
from datetime import timedelta as td
import pytz

# testing library
# tle_data = tf.read('Noaa 15')
# print(tle_data)
# quit()

# receiver position
#  The minimum elevation angle for an earth station is 8.2 degrees. 
# http://www.kt.agh.edu.pl/~kulakowski/satelity/Iridium-Leo.pdf
elBound = 10.0  # limit for lowest elevation [deg]

# time settings
startTime = dt(year=2019, month=3, day=4, hour=5, tzinfo=pytz.utc)
hoursForecast = 13
arg1 = 0
resolution = 60  # [seconds]

# input file settings (use spares[] to exclude spare Iridium satellites)
# tleFile = 'iridium-NEXT_noSPARES.DAT'
tleFile = 'iridium-NEXT.txt'
csvFile = 'satVis_' + str(startTime.day).zfill(2) + '-' + str(startTime.month).zfill(2) + '-' + str(
    startTime.year) + '_' + str(hoursForecast) + 'hours.csv'
spares = ["IRIDIUM 124", "IRIDIUM 115", "IRIDIUM 175", "IRIDIUM 176", "IRIDIUM 170", "IRIDIUM 162", "IRIDIUM 161"]

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
csv = open(csvFile, 'w')
csv.write('"minutes of the day","Sat visible Count"\r\n')  # table header
tempTime = startTime
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

    # progress bar
    if cnt >= steps / 50:
        print('#', end='', flush=True)
        cnt -= steps / 50
    cnt += 1
print("#\ndone!")

csv.close()
