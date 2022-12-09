from sr.robot3 import *
import time
R = Robot()

R.ruggeduino.pins[2].mode = INPUT_PULLUP

while True:
    if R.ruggeduino.pins[2].digital_read():
        R.kch.leds[UserLED.A].g = True
