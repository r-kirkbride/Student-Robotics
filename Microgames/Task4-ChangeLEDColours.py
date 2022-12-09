from sr.robot3 import *
import time
R = Robot()

while True:
    R.kch.leds[UserLED.A].r = True
    R.kch.leds[UserLED.B].g = True
    R.kch.leds[UserLED.C].b = True
    time.sleep(1)
    R.kch.leds[UserLED.A].r = False
    R.kch.leds[UserLED.B].g = False
    R.kch.leds[UserLED.C].b = False
    R.kch.leds[UserLED.A].b = True
    R.kch.leds[UserLED.B].r = True
    R.kch.leds[UserLED.C].g = True
    time.sleep(1)
    R.kch.leds[UserLED.A].b = False
    R.kch.leds[UserLED.B].r = False
    R.kch.leds[UserLED.C].g = False
    R.kch.leds[UserLED.A].g = True
    R.kch.leds[UserLED.B].b = True
    R.kch.leds[UserLED.C].r = True
    time.sleep(1)
    R.kch.leds[UserLED.A].g = False
    R.kch.leds[UserLED.B].b = False
    R.kch.leds[UserLED.C].r = Falsw
