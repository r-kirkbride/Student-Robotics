from RobotObject import robot
from sr.robot3 import *
import time
R = Robot(verbose=True)



print("The code ran!")
R.servo_board.servos[2].position = 1
#R.closeArms(1)

