from sr.robot3 import *
import math
import time

R = Robot()

def bulletPoint3():

    while True:
        #stats vision
        markers = R.camera.see()
        #checks if there is atleast one marker present
        if len(markers) != 0:
            #choosing first index marker to be the first marker as it is automatically the one that is closest to the camera
            firstMarker = markers[0]
            
            #works out the angle in the horizontal plane in radians (when forward of camera and marker is perpendicular)
            angle = firstMarker.spherical.rot_y
            distance = firstMarker.distance
            
            leftOfMarker = True
            if angle < 0:
                angle = abs(angle)
                leftOfMarker = False
            
            horizontalDistance = distance * math.sin(angle)
            
            print(f"""distance from middle line (mm) = {horizontalDistance} \n
            angle (degrees) = {angle * (180/math.pi)} \n
            distance to marker (mm): {distance}""")
            
            if horizontalDistance > 200:
                if leftOfMarker:
                    R.kch.leds[UserLED.A] = Colour.RED
                    R.kch.leds[UserLED.B] = Colour.OFF
                    R.kch.leds[UserLED.C] = Colour.OFF
                else:
                    R.kch.leds[UserLED.C] = Colour.RED
                    R.kch.leds[UserLED.B] = Colour.OFF
                    R.kch.leds[UserLED.A] = Colour.OFF
            else:
                R.kch.leds[UserLED.B] = Colour.BLUE
                R.kch.leds[UserLED.C] = Colour.OFF
                R.kch.leds[UserLED.A] = Colour.OFF
            
        time.sleep(1)
            
            
            
bulletPoint3()