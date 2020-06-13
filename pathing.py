#!/usr/bin/python3
#the above command is a linux directive that tells Linux to run the following
#code as python script
from ev3dev2.auto import *#This imports every library from the ev3 library
import tankMovement as tk
from math import pi
from kalman import OneVarKalmanFilter
"""
in this code the following commands appear often

while m1.is_running and m2.is_running:
    pass

this while loop is used to keep the python script synchronized whith motor movement.
this loop isnot implemented into the tank movement file because you can replace the pass
other code that you want to run while the motors are running.
"""
def findPeeks(x):
    """
    simple function to find the minimum value and the index where it happened in the list x
    """
    min = 100
    minix = 0

    for i in range(0, len(x)-2):
        if x[i] < min:
            minix = i
            min = x[i]
    min = min/100*70        #conversion from percentage to cm
    return min, minix

def getNumApp(m1,m2,s1):
    """
    this function implements a kalman filter with the variables A, B, C, Q, R, P
    after implementing the kalman filter the EV3 turns the 90 degrees and performs a
    180 degree sweep and scans for near objects with the sensor s1
    """
    A = 1
    B = 0
    C = 1
    Q = 0.005
    R = 0.05
    P = 1

    posit = []
    filt = []
    tk.turnZdeg(m1, m2, 300, -90)

    while m1.is_running and m2.is_running:
        pass

    x = s1.proximity
    kalman_filter = OneVarKalmanFilter(A, B, C, x, P, Q, R)
    tk.turnZdeg(m1, m2, 200, 180)
    """
    this while loop takes an undetermined amount of sensor readings but you can increase the
    number of readings by slowing down the 180 sweep or increasing the sweep angle
    """
    while m1.is_running and m2.is_running:
        posit.append(m1.position)
        kalman_filter.step(0, s1.proximity)
        filt.append(kalman_filter.currentState())

    min, minix = findPeeks(filt)
    tach = -1*(posit[-1] - posit[minix])

    tk.turnTach(m1, m2, 300, tach)

    while m1.is_running and m2.is_running:
        pass

    tach = (min-10)/100/(tk.motorRadius*2*pi)

    m1.run_forever(speed_sp=200)
    m2.run_forever(speed_sp=200)
    """
    after finding the apple the robot approaches the apple until it sees the apple about
    40 cm away 
    """
    while s1.proximity*70/100 > 40:
        pass
    m1.stop()
    m2.stop()
    print(findPeeks(filt))
    return posit, minix

def returnApp(m1, m2, x, ix, arm, apple):
    """
    this functions is called after the apple is picked up and needs to
    sorted into rotten and ripe
    """
    tach = x[0]-x[ix]
    #this sends the robot back to the center of its sweep radius
    tk.moveTach(m1, m2, 300, -360*0.85)
    while m1.is_running and m2.is_running:
        pass
    #this loop tries to reset the orientations of the robot to just before it stated scanning
    tk.turnTach(m1, m2, 300, tach)
    while m1.is_running and m2.is_running:
        pass
    #assuming the previous command reset the orientation the robotonly needs to turn another 90 degrees to get back to origin
    tk.turnZdeg(m1, m2, 300, -90)
    while m1.is_running and m2.is_running:
        pass
    #the robot was predetermined to travel 32 inches to get the scanning area
    tk.moveTach(m1, m2, 300, 0.8128/(2*pi*tk.motorRadius)*360)
    while m1.is_running and m2.is_running:
        pass

    """
    this decision structure tells the robot how to sort the apple after hopefully
    returning to its origin if the robot is at its orging it only need to put turn
    positive or negative 45 degrees to sort the apple
    """
    if apple == "rotten":
        tk.turnZdeg(m1, m2, 300, -45)
        while m1.is_running and m2.is_running:
            pass
        arm.run_timed(time_sp=11000, speed_sp=-500)
        while arm.is_running():
            pass
        tk.moveTach(m1, m2, 300, 2*360)
        while m1.is_running() and m2.is_running:
            pass
        tk.moveTach(m1, m2, -300, -2*360)
        while m1.is_running() and m2.is_running:
            pass
        arm.run_timed(time_sp=11000, speed_sp=500)
        while arm.is_running():
            pass
        tk.turnZdeg(m1, m2, 300, -135)
        while m1.is_running and m2.is_running:
            pass
    elif apple == "ripe":
        tk.turnZdeg(m1, m2, 300, 45)
        while m1.is_running and m2.is_running:
            pass
        arm.run_timed(time_sp=11000, speed_sp=-500)
        while arm.is_running():
            pass
        tk.moveTach(m1, m2, 300, 2*360)
        while m1.is_running() and m2.is_running:
            pass
        tk.moveTach(m1, m2, -300, -2*360)
        while m1.is_running() and m2.is_running:
            pass
        arm.run_timed(time_sp=11000, speed_sp=500)
        while arm.is_running():
            pass
        tk.turnZdeg(m1, m2, 300, 135)
        while m1.is_running and m2.is_running:
            pass
    else:
        tk.turnZdeg(m1, m2, 300, 180)
        while m1.is_running and m2.is_running:
            pass
