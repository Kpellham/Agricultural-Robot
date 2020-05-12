#!/usr/bin/python3
import time
from ev3dev2.auto import *
import statistics as stat

colorSens = ColorSensor(INPUT_2)    # ColorSensor mapped to EV3 input 2
leftTrack = Motor(OUTPUT_A)         # left-Track motor mapped to EV3 output a
rightTrack = Motor(OUTPUT_B)        # right-Track motor mapped to EV3 output b
arm = Motor(OUTPUT_C)

samp_list = [0] * 50                # Creates four lists all length 50.
r = [0] * 50                        # These lists must be initialized here
g = [0] * 50                        # as they will be filled with RGB data
b = [0] * 50                        # from the EV3 color sensor

colorSens.calibrate_white()         # Calibrate the color sensor for light conditions
print("Calibrated")
time.sleep(5)                       # 5 seconds wait to place test object

for i in range(0, 50):              # For loop to gather 50 'images' from color sensor
    sample = colorSens.rgb          # Loads sample with a tuple from the color sensor
    samp_list[i] = list(sample)     # Converts tuple into a list and then loads 'samp_list' at index 'i'
    r[i] = sample[0]                # Strips 'r' components for further processing
    g[i] = sample[1]                # Strips 'g' components for further processing
    b[i] = sample[2]                # Strips 'b' components for further processing

avg_r = stat.mean(r)                # Average of 'r' components to increase accuracy
avg_g = stat.mean(g)                # Average of 'g' components to increase accuracy
avg_b = stat.mean(b)                # Average of 'b' components to increase accuracy

# If-elseif-else statement used to determine what action should be taken based off of
# logic statements. These statements are rough estimates of r, g, and b values used to
# determine if a certain color is present

if avg_r > 250 and avg_g > 250 and avg_b > 250:
    leftTrack.run_timed(time_sp=1000, speed_sp=500)
    print("The object is white")

elif 80 < avg_r < 130 and 0 < avg_g < 100 and 0 < avg_b < 100:
    rightTrack.run_timed(time_sp=1000, speed_sp=500)
    print("The object is red")

elif 0 < avg_r < 100 and 80 < avg_g < 200 and 0 < avg_b < 100:
    arm.run_timed(time_sp=12000, speed_sp=500)
    print("The object is green")

else:
    print("Undetermined")

print("'R' Component:", avg_r)
print("'G' Component:", avg_g)
print("'B' Component:", avg_b)
