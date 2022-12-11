from sr.robot3 import *
import time

R = Robot()

R.ruggeduino.pins[A0].mode = INPUT_PULLUP
R.ruggeduino.pins[A1].mode = INPUT_PULLUP
R.ruggeduino.pins[A2].mode = INPUT_PULLUP
R.ruggeduino.pins[A3].mode = INPUT_PULLUP

R.motor_board.motors[0].power = 0.1
R.motor_board.motors[1].power = 0.1

while True:
    print(R.ruggeduino.pins[A0].analogue_read(), R.ruggeduino.pins[A1].analogue_read(), R.ruggeduino.pins[A2].analogue_read(), R.ruggeduino.pins[A3].analogue_read())
    time.sleep(0.05)
