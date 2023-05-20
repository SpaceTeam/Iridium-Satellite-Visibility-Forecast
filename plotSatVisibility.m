% Author: Tobias Neumann | RX23 Daedalus

clear;

sizeJPG = 1800; % width [px]
sizePDF = 1500;

% starting time (UTC)
year = 2023;
month = 5;
day = 19;
hour = 10;
hoursPeriod = 6.; % [h]

time_string = strcat(num2str(day, "%02d"), "-", num2str(month, "%02d"), ...
    "-", num2str(year), "_", num2str(hoursPeriod), "hours");
vals = dlmread(strcat("satVis_", time_string, ".csv"), ",", 1, 0);
x = (vals(:, 1) + hour * 60)./60.;
y = vals(:, 2);

fig = figure;

stairs(x, y);
hold all
if 1
    t_liftoff = 13+(54+39/60)/60;
    t_landing = 13+(55+50/60)/60;  
    z = 6*ones(size(y));
    idx_flight = x>t_liftoff & x<t_landing;
    area(x(idx_flight),z(idx_flight),"FaceColor","r","FaceAlpha",0.5)
end

grid on
ylim([0, 6]);
xlabel("time / h");
ylabel("[Satellites count]");
print(fig, strcat("PDF_", time_string, ".pdf"), "-dpdf", strcat("-S", num2str(sizePDF), ",", num2str(int32(sizePDF/4))));
print(fig, strcat("JPG_", time_string, ".jpg"), "-djpg", strcat("-S", num2str(sizeJPG), ",", num2str(int32(sizeJPG/4))));
% close;

