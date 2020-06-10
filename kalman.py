# https://github.com/lblackhall/pyconau2016/blob/master/kalman.py

class OneVarKalmanFilter(object):

    def __init__(self, A, B, C, x, P, Q, R):
        self.A = A                          # Process dynamics
        self.B = B                          # Control dynamics
        self.C = C                          # Measurement dynamics
        self.currentStateEstimate = x       # Current state estimate
        self.currentProbEstimate = P        # Current probability of state estimate
        self.Q = Q                          # Process covariance
        self.R = R                          # Measurement covariance

    def currentState(self):
        return self.currentStateEstimate

    def step(self, controlInput, measurement):
        # Prediction step
        predictedStateEstimate = self.A * self.currentStateEstimate + self.B * controlInput
        predictedProbEstimate = (self.A * self.currentProbEstimate) * self.A + self.Q

        # Observation step
        innovation = measurement - self.C * predictedStateEstimate
        innovationCovariance = self.C * predictedProbEstimate * self.C + self.R

        # Update step
        kalmanGain = predictedProbEstimate * self.C * 1 / float(innovationCovariance)
        self.currentStateEstimate = predictedStateEstimate + kalmanGain * innovation

        # eye(n) = nxn identity matrix.
        self.currentProbEstimate = (1 - kalmanGain * self.C) * predictedProbEstimate
