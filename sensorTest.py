#!/usr/bin/python3

from ev3dev2.auto import *
from kalman import OneVarKalmanFilter
A = 1
B = 0
C = 1
Q = 0.005
R = 1
x = 50
P = 1

kalman_filter = OneVarKalmanFilter(A, B, C, x, P, Q, R)
s1 = InfraredSensor(INPUT_1)
data = []
estimate = []
for i in range(0, 100):
    data.append(s1.proximity)

for i in data:
    kalman_filter.step(0, i)
    estimate.append(kalman_filter.currentState())

print(estimate)

