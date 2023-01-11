from sr.robot3 import *
import math
import time

R = Robot()

def bulletPoint2():

    while True:

        #camera sees and idenifies the closest Marker to it    
        markers = R.camera.see()
        if len(markers) != 0:
            firstMarker = markers[0]
            
            #calculates an angle for the marker in radians into degrees
            angle = firstMarker.orientation.rot_y * (180/math.pi)
            print(angle)

            #checks if angle is a certain value and lights up the correct LED accordingly
            if angle > 30:
                R.kch.leds[UserLED.C] = Colour.BLUE
                R.kch.leds[UserLED.A] = Colour.OFF
                R.kch.leds[UserLED.B] = Colour.OFF
            elif angle < -30:
                R.kch.leds[UserLED.A] = Colour.BLUE
                R.kch.leds[UserLED.C] = Colour.OFF
                R.kch.leds[UserLED.B] = Colour.OFF
            else:
                R.kch.leds[UserLED.B] = Colour.BLUE
                R.kch.leds[UserLED.A] = Colour.OFF
                R.kch.leds[UserLED.C] = Colour.OFF
        time.sleep(0.5)

bulletPoint2()