from sr.robot3 import *
R = Robot()
R.ruggeduiono.pins[1].mode = INPUT_PULLUP

while True:
    if R.ruggeduino.pins[1].digital_read():
        R.kch.leds[UserLED.A].g = True 