from sr.robot3 import *
import time
R = Robot()

R.ruggeduino.pins[2].mode = INPUT_PULLUP

while True:
    if not R.ruggeduino.pins[2].digital_read():
        markers = R.camera.see()

        for m in markers:
            print(" - Marker #{0} is {1} metres away".format(alpha[m.id], m.distance / 1000))

    else:
        R.kch.leds[UserLED.A].g = True
