#!/usr/bin/python3
#the above command is a linux directive that tells Linux to run the following
#code as python script
from ev3dev2.auto import *#This imports every library from the ev3 library
import tankMovement as tk
from math import pi
from kalman import OneVarKalmanFilter
def findPeeks(x):
    min = 100
    minix = 0

    for i in range(0, len(x)-2):
        if x[i] < min:
            minix = i
            min = x[i]
    min = min/100*70
    return min, minix

def getNumApp(m1,m2,s1):
    """
    this function implements a kalman filter with the variables A, B, C, Q, R, P
    after implementing the kalman filter the EV3 turns the 90 degrees and performs a
    180 degree sweep and scans for near objects with the
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
    while s1.proximity*70/100 > 40:
        pass
    m1.stop()
    m2.stop()
    print(findPeeks(filt))
    return posit, minix

def returnApp(m1, m2, x, ix, apple):

    tach = x[0]-x[ix]
    tk.moveTach(m1, m2, 300, -360*0.85)
    while m1.is_running and m2.is_running:
        pass
    tk.turnTach(m1, m2, 300, tach)
    while m1.is_running and m2.is_running:
        pass
    tk.turnZdeg(m1, m2, 300, -90)
    while m1.is_running and m2.is_running:
        pass
    tk.moveTach(m1, m2, 300, 0.8128/(2*pi*tk.motorRadius)*360)
    while m1.is_running and m2.is_running:
        pass
    if apple == "rotten":
        tk.turnZdeg(m1, m2, 300, -45)
        while m1.is_running and m2.is_running:
            pass
        tk.turnZdeg(m1, m2, 300, -135)
        while m1.is_running and m2.is_running:
            pass
    elif apple == "ripe":
        tk.turnZdeg(m1, m2, 300, 45)
        while m1.is_running and m2.is_running:
            pass
        tk.turnZdeg(m1, m2, 300, 135)
        while m1.is_running and m2.is_running:
            pass
    else:
        tk.turnZdeg(m1, m2, 300, 180)
        while m1.is_running and m2.is_running:
            pass
