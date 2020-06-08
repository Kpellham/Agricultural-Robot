#!/usr/bin/python3
#the above command is a linux directive that tells Linux to run the following
#code as python script
from ev3dev2.auto import *#This imports every library from the ev3 library
import tankMovement as tk
from kalman import OneVarKalmanFilter
def findPeeks(x):
    minix = 0
    min = 100
    for i in range(0, len(x)-1):
        if x[i]
def getNumApp(m1,m2,s1):
    A = 1
    B = 0
    C = 1
    Q = 0.005
    R = 1
    x = 50
    P = 1

    kalman_filter = OneVarKalmanFilter(A, B, C, x, P, Q, R)

    ld = []
    ld2=0
    tk.turnZdeg(m1,m2,300, 45)
    for i in range(0, 89):
       tk.turnZdeg(m1,m2,150,1)
       for i2 in range(0,99):
          ld2 = kalman_filter.step(s1.proximity)
        ld.append(ld2)

