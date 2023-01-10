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
            
            #gives distance to marker in mm
            distance = firstMarker.distance
        
            #checks what side of the marker the camera is facing
            rightOfMarker = True
            if baseAngle < 0:
                baseAngle = 90 - abs(baseAngle)
                rightOfMarker = False
            else:
                baseAngle = 90 - baseAngle
        
            #gives the distance along the ground to marker relative to the camera in mm
            baseDistance = math.cos(heightAngle) * distance
        
            #gives the horizontal component distance of the baseDistance in mm (the distance we are checking for)
            horizontalDistance = math.cos(baseAngle) * baseDistance
            print(f"""distance from middle line = {horizontalDistance} \n
            angle along the horizontal plane = {baseAngle}
            angle along the vertical plane = {heightAngle}
            right of marker?: {rightofMarker}
            distance to marker: {distance}""")
            
            #checks the horizontal distance of the marker relative to the camera and lights and turns off the LEDs accordingly
            if horizontalDistance > 200:
                if rightOfMarker:
                    R.kch.leds[UserLED.C] = Colour.RED
                    R.kch.leds[UserLED.B] = Colour.OFF
                    R.kch.leds[UserLED.A] = Colour.OFF
                else:
                    R.kch.leds[UserLED.A] = Colour.RED
                    R.kch.leds[UserLED.C] = Colour.OFF
                    R.kch.leds[UserLED.B] = Colour.OFF
            else:
                R.kch.leds[UserLED.B] = Colour.BLUE
                R.kch.leds[UserLED.C] = Colour.OFF
                R.kch.leds[UserLED.A] = Colour.OFF
            
        time.sleep(1)
            
bulletPoint3()
