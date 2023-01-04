from sr.robot3 import *
import math
import time

R = Robot()

def bulletPoint2():
    
    markers = R.camera.see()
    if len(markers) != 0:
        closestMarker = markers[0]
        for marker in markers:
            if marker.distance < closestMarker.distance:
                closestMarker = marker

    while True:

        #camera sees and idenifies the closest Marker to it    
        markers = R.camera.see()
        if len(markers) != 0:
            closestMarker = markers[0]
            for marker in markers:
                if marker.distance < closestMarker.distance:
                    closestMarker = marker
        
        
        #calculates an angle for the marker from radians into degree
        angle = closestMarker.spherical.rot_y * (180/math.pi)
        print(angle)
        
        #checks if angle is a certain value and lights up the correct LED accordingly
        if angle > 30:
            R.kch.leds[UserLED.A] = Colour.BLUE
            R.kch.leds[UserLED.C] = Colour.OFF
            R.kch.leds[UserLED.B] = Colour.OFF
        elif angle < -30:
            R.kch.leds[UserLED.C] = Colour.BLUE
            R.kch.leds[UserLED.A] = Colour.OFF
            R.kch.leds[UserLED.B] = Colour.OFF
        else:
            R.kch.leds[UserLED.B] = Colour.BLUE
            R.kch.leds[UserLED.A] = Colour.OFF
            R.kch.leds[UserLED.C] = Colour.OFF
        time.sleep(0.5)

bulletPoint2()
