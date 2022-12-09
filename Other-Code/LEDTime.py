from sr.robot3 import *
import time
R = Robot()
R.ruggeduino.pins[0].mode = INPUT_PULLUP

while True:
    if R.ruggeduino.pins[0].digital_read():
        R.kch.leds[UserLED.A].g = True
    else:
        R.kch.leds[UserLED.A].g = False


while True:
    R.kch.leds[UserLED.A].r = True
    R.kch.leds[UserLED.B].g = True
    R.kch.leds[UserLED.C].b = True
    time.sleep(1)
    R.kch.leds[UserLED.A].b = True
    R.kch.leds[UserLED.B].r = True
    R.kch.leds[UserLED.C].g = True
    time.sleep(1)
    R.kch.leds[UserLED.A].g = True
    R.kch.leds[UserLED.B].b = True
    R.kch.leds[UserLED.C].r = True
    time.sleep(1)

    R.servo_board.servos[0].position = 0.2
    time.sleep(0.5)
    R.servo_board.servos[0].position = -0.2
    time.sleep(0.5)

    R.kch.leds[UserLED.A].r = False
    R.kch.leds[UserLED.B].g = False
    R.kch.leds[UserLED.C].b = False
    time.sleep(1)
    R.kch.leds[UserLED.A].b = False
    R.kch.leds[UserLED.B].r = False
    R.kch.leds[UserLED.C].g = False
    time.sleep(1)
    R.kch.leds[UserLED.A].g = False
    R.kch.leds[UserLED.B].b = False
    R.kch.leds[UserLED.C].r = False
    time.sleep(1)
