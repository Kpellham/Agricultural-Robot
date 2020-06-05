#NextSpeed = 0                                               #NextSpeed, I, PreviousSpeed, Divisor, must be initilized on startup and will be overridden by function return
#I = 0
#PreviousSpeed = [0,0,0,0,0]
#Divisor = 0                                                            #Function call will take NextSpeed as an input

#These values need to be initialized outside of this code

from ev3dev2.auto import *

def Harvesting(NextSpeed, Divsor):
    '''
    Controls the harvesting control of the robot

    Parameters
    ----------
    NextSpeed : Int
        Indicating the next starting position for the motor speed.
    Divisor : Int
        Indicating the number of values > 0 stored in PreviousSpeed

    Yields
    ------
    NumSpeed : int
        Percent of motor speed to harvest previous apple.


    '''

    NewPosition = arm.Position                                              #Store current motor position
    NumSpeed = 20                                                           #Default motor speed (starting point)
    arm.run_timed(time_sp = 1000, speed_sp = SpeedPercent(NumSpeed))                             #Move motor for 1 sec at speed NumSpeed
    ArmPosition = arm.Position                                              #Store new motor posistion
    while ArmPosition != NewPosition:                                        #Compare the 2 position, if different stay in loop (indicating stem motion)
            NewPosition = arm.Position                                     #Check position, try to move motor, check position again
            arm.run_timed(time_sp = 500, speed_sp = SpeedPercent(NumSpeed))
            ArmPosition = arm.Position
    NewPosition = arm.Position                       #Exited loop indicating no change in position. Store position.
    if NextSpeed != 0:                               #This is used if we have a previous stored speed value from last harvest
            if Divisor != 5:                         #This is used if 5 data points have not been stored in PreviousSpeed
                NumSpeed = NextSpeed - 20       #If previous NextSpeed value, use that - 20 as starting point for harvesting speed
                arm.run_timed(time_sp = 500, speed_sp = SpeedPercent(NumSpeed))      #Try to remove apple using this speed
                ArmPosition = arm.Position              #Determine new motor position
                while ArmPosition == NewPosition:        #if no change, increase speed and try again
                        NumSpeed + 5                    #We now have a previous value to start from for increments get smaller
                        arm.run_timed(time_sp = 500, speed_sp = SpeedPercent(NumSpeed))      #Try to move arm
                        ArmPosition = arm.Position      #Determine motor position
            else:                                    #Else if 5 data points we are more sure of the nextSpeed values, smaller increments
                NumSpeed = NextSpeed - 10       #More confident in starting position so smaller intervals
                arm.run_timed(time_sp = 500, speed_sp = SpeedPercent(NumSpeed))      #Try to move motor
                ArmPosition = arm.Position         #Determine position
                while ArmPosition == NewPosition: #If no change continure to increase speed until removed
                        NumSpeed + 3             #More confidence so smaller intervals
                        arm.run_timed(time_sp = 500, speed_sp = SpeedPercent(NumSpeed))
                        ArmPosition = arm.Position
    else:
        NumSpeed + 10                           #This is used if NextSpeed is zero indicating first harvest attempt
        arm.run_timed(time_sp = 500, speed_sp = SpeedPercent(NumSpeed))              #Try to move motor
        ArmPosition = arm.Position           #Determine position
        while ArmPosition == NewPosition:        #If no change, increase speed and try again until change in position
                NumSpeed + 10
                arm.run_timed(time_sp = 500, speed_sp = SpeedPercent(NumSpeed))
                ArmPosition = arm.Position
    #Finishing Havesting motion
    arm.run_timed(time_sp = 8000, speed_sp = SpeedPercent(NumSpeed))
    return NumSpeed


def ControlArmSpeed(NumSpeed, I, PreviousSpeed):          #PreviousSpeed and I all equal zero
    '''Controls the output to the motors

    Parameters
    ----------
    NumSpeed : Int
        Previous value of percent speed of motor to harvest apple.
    I: Int
        Count of array index to store NumSpeed in PreviousSpeed array
    PreviousSpeed: array
        Int of previous harvest motor speed values

    Yields
    ------
    NextSpeed : Int
        Value used for starting speed pf motor.
    I : Int
        Count of array index to store NumSpeed in PreviousSpeed array
    Divisor: Int
        Contains the count of numbers > 0 in PreviousSpeed
    PreviousSpeed: Array
        Int of previous harvest motor speed values


    '''
    PreviousSpeed[I] = NumSpeed
    I + 1                                                   # I starts at index zero and stores Numspeed in the array then increase I value
    if I > 4:                                               #If I gets above 4 restart the count, this only stores the 5 most recent points
        I = 0
    Divisor = 0
    for i in range (0,4):                   # maybe 3
        if PreviousSpeed[i] > 0:        #Determine of many positive numbers are in the array, this will be used for average
                Divisor + 1
    NextSpeed = (PreviousSpeed[0] + PreviousSpeed[1] + PreviousSpeed[2] + PreviousSpeed[3] + PreviousSpeed[4]) / Divisor
    #Sum all elements of the array and divide by the number of stored data points
    return NextSpeed, I, Divisor, PreviousSpeed
