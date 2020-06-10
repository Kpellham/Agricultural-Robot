#!/usr/bin/python3

from ev3dev2.auto import *

m1 = Motor(OUTPUT_A)
m2 = Motor(OUTPUT_B)

infr = InfraredSensor(INPUT_1)

m1.run_forever()
m2.run_forever()
while infr.distance() > 10:#this runs the following loop until the sensor get 10 cm away from an object
    pass
m1.stop()#turns the motors off until
m2.stop()
