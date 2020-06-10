#!/usr/bin/python3
import time
from ev3dev2.auto import *
import numpy as np

colorSens = ColorSensor(INPUT_2)
colorSens.calibrate_white()

samp = np.zeros((25, 3))

for i in range(0, 24):
    samp([i,0]) += colorSens.rgb
