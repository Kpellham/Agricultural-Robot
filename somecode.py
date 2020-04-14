#!/usr/bin/pybricks-micropython
from ev3dev2.auto import *

m1 = Motor(OUTPUT_A)
m2 = Motor(OUTPUT_B)
m1.run_timed(time_sp=3000, speed_sp=500)
m2.run_timed(time_sp=3000, speed_sp=500)
