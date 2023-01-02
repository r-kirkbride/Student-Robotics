from sr.robot3 import *
import math
import time

R = Robot()

def bulletPoint3():

    #This loop makes sure that the closest marker is saved as the first marker
    markers = R.camera.see()
    if len(markers) != 0:
        firstMarker = markers[0]
        for marker in markers:
            if marker.distance < firstMarker.distance:
                firstMarker = marker
    
    while True:
        markers = R.camera.see()
        if len(markers) != 0:
            firstMarker = markers[0]
            for marker in markers:
                if marker.distance < firstMarker.distance:
                    firstMarker = marker
    
        #gives the vertical angle of marker relative to the camera in radians
        heightAngle = 90 - firstMarker.spherical.rot_x
        
        #gives the horizontal angle of marker relative to the camera in radians
        baseAngle = 90 - firstMarker.spherical.rot_y
        
        #checks what side of the marker the camera is facing
        leftOfMarker = True
        if baseAngle < 0:
            baseAngle = baseAngle + 90
            leftOfMarker = False
        
        #gives the distance along the ground to marker relative to the camera in mm
        baseDistance = math.cos(heightAngle) * firstMarker.spherical.dist
        
        #gives the horizontal component distance of the baseDistance in mm (the distance we are checking for)
        horizontalDistance = math.cos(baseAngle) * baseDistance

        #checks the horizontal distance of the marker relative to the camera and lights and turns off the LEDs accordingly
        if horizontalDistance > 200:
            if leftOfmarker:
                R.kch.leds[UserLED.A] = Colour.RED
                R.kch.leds[UserLED.B] = Colour.OFF
                R.kch.leds[UserLED.C] = Colour.OFF
            else:
                R.kch.leds[UserLED.C] = Colour.RED
                R.kch.leds[UserLED.A] = Colour.OFF
                R.kch.leds[UserLED.B] = Colour.OFF
        else:
            R.kch.leds[UserLED.B] = Colour.BLUE
            R.kch.leds[UserLED.C] = Colour.OFF
            R.kch.leds[UserLED.A] = Colour.OFF
            
        time.sleep(0.5)
            
bulletPoint3()
