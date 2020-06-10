from kalman import OneVarKalmanFilter

"""This is a function that uses the EV3 color sensor to collect data about 
the object it is evaluating. This function makes use of a Kalman filter to
smooth the, otherwise, noisy data given by the color sensor. """

def colorTester(colorSens):

    # Initialize values for the Scalar Kalman Filter
    A = 1           # No process innovation
    C = 1           # Measurement
    B = 0           # No control input
    Q = 0.005       # Covariance
    R = 1           # Measurement covariance
    x = 255/2       # Initial estimate
    P = 1           # Initial covariance

    kalmanFilter = OneVarKalmanFilter(A, B, C, x, P, Q, R)

    # Empty lists for working with data from sensor
    n = 200
    sample_list = [0] * n                # Creates four lists all length 50.
    r = [0] * n                          # These lists must be initialized here
    g = [0] * n                          # as they will be filled with RGB data
    b = [0] * n                          # from the EV3 color sensor

    # Empty lists for capturing filter estimates
    red_estimate = []
    green_estimate = []
    blue_estimate = []

    for i in range(0, n):               # For loop to gather n samples from color sensor
        sample = colorSens.rgb          # Loads sample with a tuple from the color sensor
        sample_list[i] = list(sample)   # Converts tuple into a list and then loads 'sample_list' at index 'i'
        r[i] = sample[0]                # Strips 'r' components for further processing
        g[i] = sample[1]                # Strips 'g' components for further processing
        b[i] = sample[2]                # Strips 'b' components for further processing

    """Data arriving sequentially: 
    The following for loops make use of the Kalman filter which returns the
    filtered estimate of the red, green and blue components of 'image' seen
    by the color sensor."""
    for data in r:
        kalmanFilter.step(0, data)
        red_estimate.append(kalmanFilter.currentState())

    for data in g:
        kalmanFilter.step(0, data)
        green_estimate.append(kalmanFilter.currentState())

    for data in b:
        kalmanFilter.step(0, data)
        blue_estimate.append(kalmanFilter.currentState())

    """If-elseif-else statement used to determine what action should be taken based off of
    logic statements. These statements are rough estimates of r, g, and b values used to
    determine if a certain color is present."""

    if 45 < int(red_estimate[-1]) < 120 and 75 < int(green_estimate[-1]) < 135 and 25 < int(blue_estimate[-1]) < 55:
        state = "ripe"

    elif 5 < int(red_estimate[-1]) < 75 and 5 < int(green_estimate[-1]) < 50 and 5 < int(blue_estimate[-1]) < 50:
        state = "rotten"

    else:
        state = "growing"

    print(red_estimate[-1])     # Prints the last element of the red_estimate list
    print(green_estimate[-1])   # Prints the last element of the green_estimate list
    print(blue_estimate[-1])    # Prints the last element of the blue_estimate list

    # returns the state of the apple for string comparison in the main program
    return state

