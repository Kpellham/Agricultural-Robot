import numpy as np
Height = 5
def position_arm(Height):
        '''This function takes in the "height" value of the apple from the inputs and returns the angle that
        the motor needs to be set to and the distance to set the robot to in order for the arm to grab the apple.
        A1 = length of robot arm (segment 1).
        A2 = length of robot arm (segment 2).

        Parameters
        ----------
        Height : double
            Indicating the height of the apple in inches.

        Yields
        ------
        Angle : Double
            Angle to set motor to.
        Distance : Double
            Distance to place robot for arm to grab apple.

        '''
        A1 = 8          #Length of 1st piece of arm (movable part)
        A2 = 6.75           #Length of 2nd piece of arm (Stationary part)
        ThetaRad = (np.arcsin(Height/A1))
        Theta = round((180/(np.pi))*(np.arcsin(Height/A1)), 2)
        Distance = round((A1*np.cos(ThetaRad) + A2), 3)


        return Theta, Distance

Theta, Distance = position_arm(Height)
print('Posistion motor to angle ', Theta, ' degrees')
print('Distance robot to ', Distance)
