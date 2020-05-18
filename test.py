#!/usr/bin/python3
import time
from ev3dev2.auto import *
import statistics as stat

proxSens = InfraredSensor(INPUT_1)
colorSens = ColorSensor(INPUT_2)
touchSens = TouchSensor(INPUT_3)
leftTrack = Motor(OUTPUT_A)
rightTrack = Motor(OUTPUT_B)
arm = Motor(OUTPUT_C)

def proxLoop(sensor):
    while sensor.proximity > 75:
        pass

leftTrack.run_forever()
rightTrack.run_forever()

proxloop(proxsens)

rightTrack.stop()
leftTrack.stop()

arm.run_timed(time_sp=10000, speed_sp=-500)
time.sleep(11)
leftTrack.run_timed(time_sp=750, speed_sp=500)
rightTrack.run_timed(time_sp=750, speed_sp=500)
time.sleep(1)
arm.run_timed(time_sp=10000, speed_sp=500)
