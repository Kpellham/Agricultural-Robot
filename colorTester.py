#!/usr/bin/python3
import time
from ev3dev2.auto import *
import statistics as stat

colorSens = ColorSensor(INPUT_2)
leftTrack = Motor(OUTPUT_A)
rightTrack = Motor(OUTPUT_B)
arm = Motor(OUTPUT_C)

samp_list = [0] * 50
r = [0] * 50
g = [0] * 50
b = [0] * 50

colorSens.calibrate_white()
print("Calibrated")
time.sleep(5)

for i in range(0, 50):
    sample = colorSens.rgb
    samp_list[i] = list(sample)
    r[i] = sample[0]
    g[i] = sample[1]
    b[i] = sample[2]

avg_r = stat.mean(r)
avg_g = stat.mean(g)
avg_b = stat.mean(b)

if avg_r > 250 and avg_g > 250 and avg_b > 250:
    leftTrack.run_timed(time_sp=1000, speed_sp=500)
    print("The object is white")
elif 80 < avg_r < 130 and 0 < avg_g < 100 and 0 < avg_b < 100:
    rightTrack.run_timed(time_sp=1000, speed_sp=500)
    print("The object is red")
elif 0 < avg_r < 100 and 80 < avg_g < 150 and 0 < avg_b < 100:
    arm.run_timed(time_sp=1000, speed_sp=-500)
    print("The object is green")
else:
    print("Undetermined")

print("'R' Component:", avg_r)
print("'G' Component:", avg_g)
print("'B' Component:", avg_b)
