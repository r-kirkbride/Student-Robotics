from sr.robot3 import *
import math
import time

R = Robot()

def bulletPoint3():

    while True:
        markers = R.camera.see()
        if len(markers) != 0:
            firstMarker = markers[0]
    
            #gives the vertical angle of marker relative to the camera in radians
            heightAngle = firstMarker.orientation.rot_x
        
            #gives the horizontal angle of marker relative to the camera in radians
            baseAngle = firstMarker.orientation.rot_y
        
            #checks what side of the marker the camera is facing
            leftOfMarker = True
            if baseAngle < 0:
                baseAngle = baseAngle + 90
                leftOfMarker = False
        
            #gives the distance along the ground to marker relative to the camera in mm
            baseDistance = math.cos(heightAngle) * firstMarker.distance
        
            #gives the horizontal component distance of the baseDistance in mm (the distance we are checking for)
            horizontalDistance = math.sin(baseAngle) * baseDistance
            print(horizontalDistance)
            
            #checks the horizontal distance of the marker relative to the camera and lights and turns off the LEDs accordingly
            if horizontalDistance > 200:
                if leftOfMarker:
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