from sr.robot3 import *
import math
import time

R = Robot()

def bulletPoint2():

    while True:

        #camera sees and idenifies the closest Marker to it    
        markers = R.camera.see()
        closestMarker = markers[0]

        #calculates an angle for the marker from radians into degree
        angle = closestMarker.spherical.rot_y * (180/math.pi)
        print(angle)
        
        #checks if angle is a certain value and lights up the correct LED accordingly
        if angle > 30:
            R.kch.leds[UserLED.A] = Colour.BLUE
        elif angle < -30:
            R.kch.leds[UserLED.C] = Colour.BLUE
        else:
            R.kch.leds[UserLED.B] = Colour.BLUE
    
        time.sleep(0.5)

bulletPoint2()
