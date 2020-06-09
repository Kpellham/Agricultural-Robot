from ev3dev2.auto import *
from math import pi
motorRadius = 0.015#i require the radius of motors for further calculations of the Agribot movement
motordis = 0.081#I require the distance between the motors so im setting this value to zero for now

def turnRadius(m1, m2, r, speedI, dis, time):
    speedO = speedI * r * (r+dis) / r#this equation relates the speed of the inner an outer track of the Agribot
    m1.run_timed(time_sp = time, speed_sp = speedI)
    m2.run_times(time_sp = time, speed_sp = speedO)

def turnZ(m1, m2,  speed, time):
    m1.run_timed(time_sp = time, speed_sp = speed)
    m2.run_timed(time_sp = time, speed_sp = -1*speed)
def turnZdeg(m1, m2, speed, deg):
    rad = deg*2/360
    rot = rad*motordis/motorRadius
    fac = m1.count_per_rot/2
    m1.run_to_rel_pos(position_sp=fac*rot,speed_sp=speed)
    m2.run_to_rel_pos(position_sp=-1*fac*rot,speed_sp=-1*speed)

def turnTach(m1, m2, speed, tacho):
    m1.run_to_rel_pos(speed_sp=speed, position_sp=tacho)
    m2.run_to_rel_pos(speed_sp=-1*speed, position_sp=-1*tacho)

def moveTach(m1, m2, speed, tacho):
    m1.run_to_rel_pos(speed_sp=speed, position_sp=tacho)
    m2.run_to_rel_pos(speed_sp=speed, position_sp=tacho)



