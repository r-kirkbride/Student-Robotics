import time
from sr.robot3 import *
R = Robot()

print("hello world")

print(f"{str(len(dir(int))-2)}kn{R(auto_start=True).motor_board.serial_number[0]}")

R.kch.leds[UserLED.A].r = True 

while True:
    R.kch.leds[UserLED.A].r = True 
    time.sleep(1)
    R.kch.leds[UserLED.A].g = True 
    time.sleep(1)
    R.kch.leds[UserLED.A].b = True 
    time.sleep(1)
