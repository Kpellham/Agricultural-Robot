#!/usr/bin/python3
from ev3dev2.auto import *

arm = Motor(OUTPUT_C)
# nextspeed = 76
# divisor = 5
# count = 4                                                                  # These values must be declared outside of function
# previous_speed_input = [85,82,75,71,68]                                          # at the startup of robot

# arm.on_for_seconds(SpeedPercent(-40), 9)                                    # Lowers arm to grab apple
def harvesting(nextspeed, divisor):

    # Controls the harvesting control of the robot

    # Parameters

    # nextspeed : Int
        # Indicating the next starting percentage for the motor speed.
    # divisor : Int
        # Indicating the number of values > 0 stored in previous_speed

    # Yields

    # numspeed : int
        # Percent of motor speed required to harvest previous apple.

    time_count = 0
    newposition = arm.position                                              # Store current motor position
    numspeed = 20                                                           # Default motor speed (starting point)
    arm.on_for_seconds(SpeedPercent((numspeed+20)), 5)                      # This controls the grabber mechanism to close onto the apple
    armposition = arm.position                                              # Store new motor position
    while armposition != newposition:                                       # Compare the 2 position, if different stay in loop (indicating stem motion)
        newposition = arm.position                                          # Check position, try to move motor, check position again
        arm.on_for_seconds(SpeedPercent((numspeed - 10)), 1)                # This section represents the extension of the stem
        armposition = arm.position
        time_count = time_count + 1
        if time_count > 17:
            print("No Results")
            return numspeed
    newposition = arm.position                                              # Exited loop indicating no change in position. Apple fully extented on stem. Store position.
    if nextspeed != 0:                                                      # This is used if we have a previous stored speed value from last harvest
        if divisor != 5:                                                    # This is used if 5 data points have not been stored in previous_speed
            numspeed = nextspeed - 20                                       # If previous nextspeed value exists, use that - 20 as starting point for harvesting speed
            arm.on_for_seconds(SpeedPercent(numspeed), .5)                  # Try to remove apple using this speed
            armposition = arm.position                                      # Determine new motor position
            while armposition == newposition:                               # if no change, increase speed and try again
                numspeed = numspeed + 5                                     # We now have a previous value to start from so the increments get smaller
                if numspeed > 90:                                           # Cannot exceed a value of 100 percent
                    numspeed = nextspeed - 20
                arm.on_for_seconds(SpeedPercent(numspeed), 0.5)             # Try to move arm
                armposition = arm.position                                  # Determine motor position
        else:                                                               # Else if 5 data points we are more sure of the nextSpeed values, smaller increments
            numspeed = nextspeed - 10                                       # More confident in starting position so smaller intervals
            arm.on_for_seconds(SpeedPercent(numspeed), .5)                  # Try to move motor
            armposition = arm.position                                      # Determine position
            while armposition == newposition:                               # If no change continue to increase speed until removed
                numspeed = numspeed + 3                                     # More confidence so smaller intervals
                if numspeed > 90:                                           # Cannot exceed a value of 100 percent
                    numspeed = nextspeed - 10
                arm.on_for_seconds(SpeedPercent(numspeed), .5)
                armposition = arm.position
    else:
        numspeed = numspeed + 10                                            # This is used if nextspeed is zero indicating first harvest attempt
        arm.on_for_seconds(SpeedPercent(numspeed), .5)                       # Try to move motor
        armposition = arm.position                                          # Determine position
        while armposition == newposition:                                   # If no change, increase speed and try again until change in position
            numspeed = numspeed + 10
            if numspeed > 90:                                               # Cannot exceed 100 percent
                numspeed = 40
            arm.on_for_seconds(SpeedPercent(numspeed), .5)
            armposition = arm.position
        # Finishing Havesting motion
    arm.on_for_seconds(SpeedPercent(numspeed), 1)              # Apple is now removed from stem and tree so run modor to fully vertical position
    print("Required percentage to remove apple was ", numspeed)
    return numspeed


def control_arm_speed(numspeed, count, previous_speed_input):          # PreviousSpeed and count all equal zero
    # Controls the output to the motors

    # Parameters

    # numspeed : Int
        # Previous value of percent speed of motor to harvest apple.
    # count: Int
        # Count of array index to store NumSpeed in PreviousSpeed array
    # previous_speed_input: array
        # Int of previous harvest motor speed values

    # Yields

    # nextspeed : Int
        # Value used for starting speed pf motor.
    # count : Int
        # Count of array index to store NumSpeed in PreviousSpeed array
    # divisor: Int
        # Contains the count of numbers > 0 in PreviousSpeed
    # previous_speed: Array
        # Int of previous harvest motor speed values

    previous_speed = []
    previous_speed.extend(previous_speed_input)
    previous_speed[count] = numspeed
    count = count + 1                                                   # Count starts at index zero and stores Numspeed in the array then increase I value
    if count > 4:                                               # If Count gets above 4 restart the count, this only stores the 5 most recent points
        count = 0
    divisor = 0
    for i in range(0, 5):
        if previous_speed[i] > 0:        # Determine number of positive numbers are in the array, this will be used for average
            divisor = divisor + 1
    sum_speed = previous_speed[0]+previous_speed[1]+previous_speed[2]+previous_speed[3]+previous_speed[4]
    nextspeed = sum_speed/divisor                # Sum all elements of the array and divide by the number of stored data points
    print("next speed setting is" , nextspeed)
    for i in range(0, 5):
        print(previous_speed[i])

    return nextspeed, count, divisor, previous_speed

