#!/usr/bin/python3

import time
from ev3dev2.auto import *
from ControlFunctions import control_arm_speed
from ControlFunctions import harvesting
from colorTester import colorTester

# proxSens = InfraredSensor(INPUT_1)
colorSens = ColorSensor(INPUT_3)    # ColorSensor mapped to EV3 input 2
leftTrack = Motor(OUTPUT_A)         # left-Track motor mapped to EV3 output a
rightTrack = Motor(OUTPUT_B)        # right-Track motor mapped to EV3 output b
arm = Motor(OUTPUT_C)

nextSpeed = 0
divisor = 0
count = 0
previous_speed = [0, 0, 0, 0, 0]

while not arm.is_stalled:
    arm.run_forever(speed_sp=-500)
arm.stop()

print("Time to calibrate white")
time.sleep(5)
colorSens.calibrate_white()         # Calibrate the color sensor for light condition
print("Calibrated")
time.sleep(5)

while not arm.is_stalled:
    arm.run_forever(speed_sp=500)
arm.stop()

# TODO - KYLE

while True:
    while not arm.is_stalled:
        arm.run_forever(speed_sp=-500)
    arm.stop()

    if colorTester(colorSens) == "ripe":
        print("ripe")
        numSpeed = harvesting(nextSpeed, divisor, arm)
        nextSpeed, count, divisor, previous_speed = control_arm_speed(numSpeed, count, previous_speed)
        time.sleep(1)
        # TODO - Kyle
    elif colorTester(colorSens) == "rotten":
        print("rotten")
        numSpeed = harvesting(nextSpeed, divisor, arm)
        nextSpeed, count, divisor, previous_speed = control_arm_speed(numSpeed, count, previous_speed)
        time.sleep(1)
        # TODO - Kyle
    else:
        pass
        print("pass")
        # TODO - Kyle
