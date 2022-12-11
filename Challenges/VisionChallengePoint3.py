from sr.robot3 import *
import math
import time

R = Robot()

def bulletPoint3():
    markers = R.camera.see()
    firstMarker = markers[0]
    for marker in markers:
        if marker.distance < firstMarker.distance:
            firstMarker = marker
    
    while True:
        markers = R.camera.see()
        if firstMarker in markers:
            angle = firstMarker.spherical.rot_y * (180/math.pi)

            if math.sin(angle) * firstMarker.distance > 200:
                R.kch.leds[UserLED.A] = Colour.RED
            elif math.sin(angle) * firstMarker.distance < -200:
                R.kch.leds[UserLED.C] = Colour.RED
            else:
                R.kch.leds[UserLED.B] = Colour.RED
            
            time.sleep(0.5)
            R.kch.leds[UserLED.A] = Colour.OFF
            R.kch.leds[UserLED.B] = Colour.OFF
            R.kch.leds[UserLED.C] = Colour.OFF



