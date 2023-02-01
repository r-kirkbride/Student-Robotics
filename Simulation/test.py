from sr.robot3 import *

R = Robot()

# both motors foward at half speed
R.motor_board.motors[0].power = 0.5
R.motor_board.motors[1].power = 0.5

# sleep for 4 seconds
R.sleep(4)

# both motors reverse at half speed
R.motor_board.motors[0].power = -0.5
R.motor_board.motors[1].power = -0.5

# sleep for 2 seconds
R.sleep(2)

# both motors stop
R.motor_board.motors[0].power = 0
R.motor_board.motors[1].power = 0

print("Robot Finished")
