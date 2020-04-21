#!/usr/bin/python3
#the above command is a linux directive that tells Linux to run the following
#code as python script
from ev3dev2.auto import *#This imports every library from the ev3 library

m1 = Motor(OUTPUT_A)#this command tells the the EV3 brick that a motor will be
#connected to output a
m1.run_timed(time_sp=7000, speed_sp=750)#this command runs the arm for 7 seconds
