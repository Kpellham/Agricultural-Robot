#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from kalman import OneVarKalmanFilter

# RGB random data
red_random_data = np.random.normal(240, 1, size=(1, 200)).flatten()
green_random_data = np.random.normal(67, 1, size=(1, 200)).flatten()
blue_random_data = np.random.normal(128, 1, size=(1, 200)).flatten()

# Initialize values for the Kalman Filter
A = 1           # No process innovation
C = 1           # Measurement
B = 0           # No control input
Q = 0.005       # Covariance
R = 1           # Measurement covariance
x = 255/2       # Initial estimate
P = 1           # Initial covariance

kalmanFilter = OneVarKalmanFilter(A, B, C, x, P, Q, R)

# Empty lists for capturing filter estimates
red_kalman_filter_estimates = []
green_kalman_filter_estimates = []
blue_kalman_filter_estimates = []

# Simulate the data arriving sequentially
for data in red_random_data:
    kalmanFilter.step(0, data)
    red_kalman_filter_estimates.append(kalmanFilter.currentState())

for data in green_random_data:
    kalmanFilter.step(0, data)
    green_kalman_filter_estimates.append(kalmanFilter.currentState())

for data in blue_random_data:
    kalmanFilter.step(0, data)
    blue_kalman_filter_estimates.append(kalmanFilter.currentState())

# Plot results
plt.title('RGB Values')
plt.xlabel('Sample')
plt.ylabel('Value')
plt.plot(red_random_data, 'r*')
plt.plot(green_random_data, 'g*')
plt.plot(blue_random_data, 'b*')
plt.plot(red_kalman_filter_estimates, 'r')
plt.plot(green_kalman_filter_estimates, 'g')
plt.plot(blue_kalman_filter_estimates, 'b')

# Print last value from the Kalman Filter
print(red_kalman_filter_estimates[-1])
print(green_kalman_filter_estimates[-1])
print(blue_kalman_filter_estimates[-1])

plt.show()
