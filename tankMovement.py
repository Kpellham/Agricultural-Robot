from ev3dev2.auto import *
class tankMovement:

    motorRadius = 0#i require the radius of motors for further calculations of the Agribot movement
    motordis = 0#I require the distance between the motors so im setting this value to zero for now

    def turnRadius(self, m1, m2, r, speedI, dis, time):
        speedO = speedI * r * (r+dis) / r#this equation relates the speed of the inner an outer track of the Agribot
        m1.run_timed(time_sp = time, speed_sp = speedI)
        m2.run_times(time_sp = time, speed_sp = speedO)

    def turnZ(self, m1, m2,  speed, time):
        m1.run_timed(time_sp = time, speed_sp = speed)
        m2.run_timed(time_sp = time, speed_sp = -1*speed)
