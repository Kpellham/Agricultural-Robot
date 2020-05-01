#!/usr/bin/python3
import time
from ev3dev2.auto import *

s1 = ColorSensor(INPUT_2)
s1.calibrate_white()
print("ok")
time.sleep(5)
print(str(s1.rgb))

