#!/usr/bin/python3
import time
from ev3dev2.auto import *
from kalman import OneVarKalmanFilter

def colorDetector(colorSens):
    #colorSens = ColorSensor(INPUT_2)    # ColorSensor mapped to EV3 input 2
    #leftTrack = Motor(OUTPUT_A)         # left-Track motor mapped to EV3 output a
    #rightTrack = Motor(OUTPUT_B)        # right-Track motor mapped to EV3 output b
    #arm = Motor(OUTPUT_C)

    # Initialize values for the Kalman Filter
    A = 1           # No process innovation
    C = 1           # Measurement
    B = 0           # No control input
    Q = 0.005       # Covariance
    R = 1           # Measurement covariance
    x = 255/2       # Initial estimate
    P = 1           # Initial covariance

    kalmanFilter = OneVarKalmanFilter(A, B, C, x, P, Q, R)

    n = 200

    # Empty lists for working with data from sensor
    sample_list = [0] * n                # Creates four lists all length 50.
    r = [0] * n                          # These lists must be initialized here
    g = [0] * n                          # as they will be filled with RGB data
    b = [0] * n                          # from the EV3 color sensor

    # Empty lists for capturing filter estimates
    red_estimate = []
    green_estimate = []
    blue_estimate = []

    colorSens.calibrate_white()         # Calibrate the color sensor for light conditions
    print("Calibrated")
    time.sleep(5)                       # 5 seconds wait to place test object

    for i in range(0, n):             # For loop to gather 50 'images' from color sensor
        sample = colorSens.rgb          # Loads sample with a tuple from the color sensor
        sample_list[i] = list(sample)   # Converts tuple into a list and then loads 'samp_list' at index 'i'
        r[i] = sample[0]                # Strips 'r' components for further processing
        g[i] = sample[1]                # Strips 'g' components for further processing
        b[i] = sample[2]                # Strips 'b' components for further processing

    # Simulate the data arriving sequentially
    for data in r:
        kalmanFilter.step(0, data)
        red_estimate.append(kalmanFilter.currentState())

    for data in g:
        kalmanFilter.step(0, data)
        green_estimate.append(kalmanFilter.currentState())

    for data in b:
        kalmanFilter.step(0, data)
        blue_estimate.append(kalmanFilter.currentState())

    # If-elseif-else statement used to determine what action should be taken based off of
    # logic statements. These statements are rough estimates of r, g, and b values used to
    # determine if a certain color is present

    if 30 < int(red_estimate[-1]) < 135 and 75 < int(green_estimate[-1]) < 150 and 10 < int(blue_estimate[-1]) < 70:
        state = "ripe"

    elif 0 < int(red_estimate[-1]) < 75 and 0 < int(green_estimate[-1]) < 50 and 0 < int(blue_estimate[-1]) < 50:
        state = "rotten"

    else:
        state = "growing"

    return state

# Print last value from the Kalman Filter
# print(red_estimate[-1])
# print(green_estimate[-1])
# print(blue_estimate[-1])
