import time
from sr.robot3 import *

R = Robot()
ruggeduino = R.ruggeduino
while True:
    time.sleep(1)
    left = ruggeduino.command("x")
    print(f"Left Motor: {left} degrees")
    right = ruggeduino.command("y")
    print(f"Right Motor: {right} degrees")