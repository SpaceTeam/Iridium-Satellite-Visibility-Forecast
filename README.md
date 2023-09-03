# Iridium Satellite Visibility Forecast

Tool to plot a prediction of the amount of visible Iridium satellites depending on Geo-Coordinates and time. Be sure to have up-to-date TLEs of the Iridium sats at the ready. See `requirements.txt` for required Python 3 packages for the `visibility.py` script, which produces a CSV file for the set time resolution. `plotSatVisibility.m` can be used to produce JPGs and PDFs plots out of it (written with GNU Octave).

See following URLs to get TLEs from current Iridium satellites:
- https://www.celestrak.com/NORAD/elements/iridium-NEXT.txt
- https://celestrak.org/NORAD/elements/gp.php?GROUP=iridium&FORMAT=tle
- https://celestrak.org/NORAD/elements/table.php?GROUP=iridium-NEXT&FORMAT=tle

To validate the output, countercheck with https://iridiumwhere.com/