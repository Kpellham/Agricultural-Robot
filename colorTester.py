#!/usr/bin/python3
import time
from ev3dev2.auto import *
import statistics as stat

colorSens = ColorSensor(INPUT_2)
samp_list = [[] for j in range(49)]
r = [[] for j in range(49)]
g = [[] for j in range(49)]
b = [[] for j in range(49)]

colorSens.calibrate_white()
print("Calibrated")
time.sleep(5)

for i in range(0, 49):
    samp = colorSens.rgb
    samp_list[i] = list(samp)
    r[i] = samp[0]
    g[i] = samp[1]
    b[i] = samp[2]

avg_r = stat.mean(r)
avg_g = stat.mean(g)
avg_b = stat.mean(b)

if avg_r > 250 and avg_g > 250 and avg_b > 250:
    print("The object is white")
elif 100 < avg_r < 150 and 0 < avg_g < 100 and 0 < avg_b < 100:
    print("The object is red")
else:
    print("Undetermined")

print("'R' Component:", avg_r)
print("'G' Component:", avg_g)
print("'B' Component:", avg_b)
