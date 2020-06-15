#!/usr/bin/python3

import time
from ev3dev2.auto import *
from ControlFunctions import control_arm_speed
from ControlFunctions import harvesting
from colorTester import colorTester
import pathing as sc

proxSens = InfraredSensor(INPUT_1)
colorSens = ColorSensor(INPUT_3)    # ColorSensor mapped to EV3 input 2
leftTrack = Motor(OUTPUT_A)         # left-Track motor mapped to EV3 output a
rightTrack = Motor(OUTPUT_B)        # right-Track motor mapped to EV3 output b
arm = Motor(OUTPUT_C)

nextSpeed = 0
divisor = 0
count = 0
previous_speed = [0, 0, 0, 0, 0]

run = 0

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
#this value is amount of tachos required to move a linear distane of 32 inches
tach = 0.8128/(2*sc.pi*sc.tk.motorRadius)*360
"""
this for loop runs the apple finding algorithm 4 times. however because of
compounding error the robot may need to be reset to origin after each run
"""
for i in range(0, 3):

    #the robot was predetermined to move 32 inches to get to the scanning area
    sc.tk.moveTach(leftTrack, rightTrack, 300, tach)
    while leftTrack.is_running and rightTrack.is_running:
        pass
    #after getting to the scanning area a scan is performed
    posit, minix = sc.getNumApp(leftTrack, rightTrack, proxSens)

    # next 3 movements are made to get the motor in optimal position to grab the apple
    sc.tk.moveTach(leftTrack, rightTrack, 299, -360*2)
    while leftTrack.is_running and rightTrack.is_running:
        pass

    while not arm.is_stalled:
        arm.run_forever(speed_sp=-500)
    arm.stop()

    sc.tk.moveTach(leftTrack, rightTrack, 300, 360*2.85)
    while leftTrack.is_running and rightTrack.is_running:
        pass

    run1 = 0        #run is a sentinel variable to get the robot to scan for apples
    while run1 < 2:
        """
        this decision structure should only run once if the apple is decided to be ripe or rotten
        but the code should run twice if the apple is decided to be a pass. this is decided to
        add redundancy so the code has less error
        """
        if colorTester(colorSens) == "ripe":
            print("ripe")
            numSpeed = harvesting(nextSpeed, divisor, arm)
            nextSpeed, count, divisor, previous_speed = control_arm_speed(numSpeed, count, previous_speed)
            time.sleep(1)
            sc.returnApp(leftTrack, rightTrack, posit, minix, "ripe")
            run1 = run1 + 1
        elif colorTester(colorSens) == "rotten":
            print("rotten")
            numSpeed = harvesting(nextSpeed, divisor, arm)
            nextSpeed, count, divisor, previous_speed = control_arm_speed(numSpeed, count, previous_speed)
            time.sleep(1)
            sc.returnApp(leftTrack, rightTrack, posit, minix, "rotten")
            run1 = run1 + 1
        else:
            print("pass")
            run = run + 1
            if run == 3:
                run = 0
                sc.returnApp(leftTrack, rightTrack, posit, minix, "pass")
        run1 = run1 + 1
