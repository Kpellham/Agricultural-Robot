#!/usr/bin/python3

import time
from ev3dev2.auto import *
from ControlFunctions import control_arm_speed
from ControlFunctions import harvesting
from colorTester import colorTester
import somecode as sc

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

# TODO - KYLE

tach = 0.8128/(2*sc.pi*sc.tk.motorRadius)*360
sc.tk.moveTach(leftTrack, rightTrack, 300, tach)
while leftTrack.is_running and rightTrack.is_running:
    pass
posit, minix = sc.getNumApp(leftTrack, rightTrack, proxSens)

sc.tk.moveTach(leftTrack, rightTrack, 299, -360*2)
while leftTrack.is_running and rightTrack.is_running:
    pass

while not arm.is_stalled:
    arm.run_forever(speed_sp=-500)
arm.stop()

sc.tk.moveTach(leftTrack, rightTrack, 300, 360*2.85)
while leftTrack.is_running and rightTrack.is_running:
    pass

while True:

    if colorTester(colorSens) == "ripe":
        print("ripe")
        numSpeed = harvesting(nextSpeed, divisor, arm)
        nextSpeed, count, divisor, previous_speed = control_arm_speed(numSpeed, count, previous_speed)
        time.sleep(1)
        # TODO - Kyle
        sc.returnApp(leftTrack, rightTrack, posit, minix, "ripe")
    elif colorTester(colorSens) == "rotten":
        print("rotten")
        numSpeed = harvesting(nextSpeed, divisor, arm)
        nextSpeed, count, divisor, previous_speed = control_arm_speed(numSpeed, count, previous_speed)
        time.sleep(1)
        # TODO - Kyle
        sc.returnApp(leftTrack, rightTrack, posit, minix, "rotten")
    else:
        run = run + 1
        if run == 3:
            run = 0
            sc.returnApp(leftTrack, rightTrack, posit, minix, "pass")
        print("pass")
        # TODO - Kyle
