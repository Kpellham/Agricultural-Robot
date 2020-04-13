from ev3dev2.auto import *
import time

m = Motor(OUTPUT_A)
m.run_timed(time_sp=3000, speed_sp=500)


