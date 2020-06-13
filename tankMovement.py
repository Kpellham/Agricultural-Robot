from ev3dev2.auto import *
from math import pi
motorRadius = 0.015#i require the radius of motors for further calculations of the Agribot movement
motordis = 0.081#I require the distance between the motors so im setting this value to zero for now

def turnRadius(m1, m2, r, speedI, dis, time):
    """
    this function takes a radius for the robot to turn around and relates inner track
    speed to outer track speed to achieve proper turning
    """
    speedO = speedI * r * (r+dis) / r#this equation relates the speed of the inner an outer track of the Agribot

    m1.run_timed(time_sp = time, speed_sp = speedI)
    m2.run_times(time_sp = time, speed_sp = speedO)

def turnZ(m1, m2,  speed, time):
    """
    rotates the robot around it central z-axis for a set amount of time
    """
    m1.run_timed(time_sp = time, speed_sp = speed)
    m2.run_timed(time_sp = time, speed_sp = -1*speed)

def turnZdeg(m1, m2, speed, deg):
    """
    this functions takes an angle in degrees and converts it to motor rotations
    and with the motor rotations the robot turns the set amount of degrees
    """
    rad = deg*2/360                 #converting degree to pi radians
    rot = rad*motordis/motorRadius  #converts radians to motor rotations
    fac = m1.count_per_rot/2        #this factor converts radians to tachos

    m1.run_to_rel_pos(position_sp=fac*rot,speed_sp=speed)
    m2.run_to_rel_pos(position_sp=-1*fac*rot,speed_sp=-1*speed)

def turnTach(m1, m2, speed, tacho):
    """
    function that turns the robot a set amount of tachos around its central z-axis
    """
    m1.run_to_rel_pos(speed_sp=speed, position_sp=tacho)
    m2.run_to_rel_pos(speed_sp=-1*speed, position_sp=-1*tacho)

def moveTach(m1, m2, speed, tacho):
   """
   this function moves the robot linearly for a set amount of tachos
   """
    m1.run_to_rel_pos(speed_sp=speed, position_sp=tacho)
    m2.run_to_rel_pos(speed_sp=speed, position_sp=tacho)



