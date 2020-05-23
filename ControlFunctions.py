from ev3dev2.auto import *

# next_speed = 0                      # NextSpeed, I, previous_speed, Divisor, must be initialized on startup and will be overridden by function return
# count = 0
# previous_speed = [0, 0, 0, 0, 0]
# divisor = 0

# These values need to be initialized outside of this code

arm = Motor(OUTPUT_C)


def harvesting(nextspeed, divisor):
    '''
    Controls the harvesting control of the robot

    Parameters
    ----------
    nextspeed : Int
        Indicating the next starting position for the motor speed.
    divisor : Int
        Indicating the number of values > 0 stored in PreviousSpeed

    Yields
    ------
    numspeed : int
        Percent of motor speed to harvest previous apple.


    '''

    newposition = arm.position                                              # Store current motor position
    numspeed = 20                                                           # Default motor speed (starting point)
    arm.on_for_seconds(SpeedPercent(numspeed), 1)            # Move motor for 1 sec at speed NumSpeed
    armposition = arm.position                                              # Store new motor position
    while armposition != newposition:                                       # Compare the 2 position, if different stay in loop (indicating stem motion)
        newposition = arm.position                                          # Check position, try to move motor, check position again
        arm.on_for_seconds(SpeedPercent(numspeed), .5)
        armposition = arm.position
    newposition = arm.position                                              # Exited loop indicating no change in position. Store position.
    if nextspeed != 0:                                                      # This is used if we have a previous stored speed value from last harvest
        if divisor != 5:                                                    # This is used if 5 data points have not been stored in PreviousSpeed
            numspeed = nextspeed - 20                                       # If previous NextSpeed value exists, use that - 20 as starting point for harvesting speed
            arm.on_for_seconds(SpeedPercent(numspeed), .5)       # Try to remove apple using this speed
            armposition = arm.position                                      # Determine new motor position
            while armposition == newposition:                               # if no change, increase speed and try again
                numspeed = numspeed + 5                                     # We now have a previous value to start from so the increments get smaller
                arm.on_for_seconds(SpeedPercent(numspeed), .5)        # Try to move arm
                armposition = arm.position                                  # Determine motor position
        else:                                                               # Else if 5 data points we are more sure of the nextSpeed values, smaller increments
            numspeed = nextspeed - 10                                       # More confident in starting position so smaller intervals
            arm.on_for_seconds(SpeedPercent(numspeed), .5)       # Try to move motor
            armposition = arm.position                                      # Determine position
            while armposition == newposition:                               # If no change continue to increase speed until removed
                numspeed = numspeed + 3                                     # More confidence so smaller intervals
                arm.on_for_seconds(SpeedPercent(numspeed), .5)
                armposition = arm.position
    else:
        numspeed = numspeed + 10                                            # This is used if NextSpeed is zero indicating first harvest attempt
        arm.on_for_seconds(SpeedPercent(numspeed), .5)           # Try to move motor
        armposition = arm.position                                          # Determine position
        while armposition == newposition:                                   # If no change, increase speed and try again until change in position
            numspeed = numspeed + 10
            arm.on_for_seconds(SpeedPercent(numspeed), .5)
            armposition = arm.position
    # Finishing Havesting motion
    arm.on_for_seconds(SpeedPercent(numspeed), 8)              #Apple is now removed from stem and tree so run modor to fully vertical position
    return numspeed


def control_arm_speed(numspeed, count, previous_speed_input):          # PreviousSpeed and count all equal zero
    '''Controls the output to the motors

    Parameters
    ----------
    numspeed : Int
        Previous value of percent speed of motor to harvest apple.
    count: Int
        Count of array index to store NumSpeed in PreviousSpeed array
    previous_speed_input: array
        Int of previous harvest motor speed values

    Yields
    ------
    nextspeed : Int
        Value used for starting speed pf motor.
    count : Int
        Count of array index to store NumSpeed in PreviousSpeed array
    divisor: Int
        Contains the count of numbers > 0 in PreviousSpeed
    previous_speed: Array
        Int of previous harvest motor speed values


    '''
    previous_speed = []
    previous_speed.append(previous_speed_input)
    previous_speed[count] = numspeed
    count = count + 1                                                   # I starts at index zero and stores Numspeed in the array then increase I value
    if count > 4:                                               # If I gets above 4 restart the count, this only stores the 5 most recent points
        count = 0
    divisor = 0
    for i in range(0, 4):                   # maybe 3
        if previous_speed[i] > 0:        # Determine number of positive numbers are in the array, this will be used for average
            divisor = divisor + 1
    sum_speed = previous_speed[0]+previous_speed[1]+previous_speed[2]+previous_speed[3]+previous_speed[4]
    nextspeed = sum_speed/divisor
    # Sum all elements of the array and divide by the number of stored data points
    return nextspeed, count, divisor, previous_speed
