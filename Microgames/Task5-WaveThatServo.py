from sr.robot3 import *
import time
R = Robot()

while True:
    R.servo_board.servos[0].position = 0.2
    time.sleep(0.5)
    R.servo_board.servos[0].position = -0.2
    time.sleep(0.5)
