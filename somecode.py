#!/usr/bin/env pybricks-micropython
from ev3dev.auto import *

m = Motor(OUTPUT_A)
m.run_timed(time_sp=3000, speed_sp=500)
