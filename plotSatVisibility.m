# Author: Tobias Neumann | RX23 Daedalus

clear;

pkg load signal;

sizeJPG = 1800; # width [px]
sizePDF = 1500;

# starting time (UTC)
year = 2019;
month = 3;
day = 4;
hour = 5;
hoursPeriod = 13.; # [h]

time_string = strcat(num2str(day, "%02d"), "-", num2str(month, "%02d"), ...
    "-", num2str(year), "_", num2str(hoursPeriod), "hours");
vals = dlmread(strcat("satVis_", time_string, ".csv"), ",", 1, 0);
x = (vals(:, 1) + hour * 60)./60.;
y = vals(:, 2);

fig = figure(1, "visible", "off");

# make a smoothen line
xspline = linspace(min(x), max(x), (max(x) - min(x)) * 1);
yspline = interp1(x, y, xspline, "spline");

x_date = datenum(0, 1, 1, x);
plot(x_date, y);
hold on;
ysmooth = sgolayfilt(y, 3, 29);
plot(x_date, ysmooth);
ylin = medfilt1(ysmooth, 3);
plot(x_date, ylin);
legend("raw", "sgolay(raw)", "lin(sgolay(raw))");
ylim([0, 6]);#(max(vals(:, 2)) + 1)]);
tickWidth = (max(x_date) - min(x_date)) / hoursPeriod;
tickMaxAddup = (60. / 59. - 1.) / hoursPeriod;
tickWidthFactor = 1. + tickMaxAddup;
set(gca,'XTick',min(x_date):(tickWidth * tickWidthFactor):(max(x_date) + tickMaxAddup));
datetick('x', 'HH:MM', "keepticks");
xlim([min(x_date), (max(x_date) + tickMaxAddup)]);

xlabel("[hh:mm]");
ylabel("[Satellites count]");
print(fig, strcat("PDF_", time_string, ".pdf"), "-dpdf", strcat("-S", num2str(sizePDF), ",", num2str(int32(sizePDF/4))));
print(fig, strcat("JPG_", time_string, ".jpg"), "-djpg", strcat("-S", num2str(sizeJPG), ",", num2str(int32(sizeJPG/4))));

close;

