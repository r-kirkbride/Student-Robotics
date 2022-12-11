from sr.robot3 import *
import math
import time

R = Robot()

def bulletPoint3():

    #This loop makes sure that the closest marker is saved as the first marker
    markers = R.camera.see()
    firstMarker = markers[0]
    for marker in markers:
        if marker.distance < firstMarker.distance:
            firstMarker = marker
    
    while True:
        markers = R.camera.see()
        #this first ensures that the marker spotted is in the list of markers seen
        if firstMarker in markers:
            #Converts the angle recieved by the camera from raidans to degrees to ensure the math library can perfrom trig on them
            angle = firstMarker.spherical.rot_y * (180/math.pi)

            #checks the horizontal distance of the marker relative to the camera and lights and turns off the LEDs accordingly 
            if math.sin(angle) * firstMarker.distance > 200:
                R.kch.leds[UserLED.A] = Colour.RED
                R.kch.leds[UserLED.B] = Colour.OFF
                R.kch.leds[UserLED.C] = Colour.OFF
            
            elif math.sin(angle) * firstMarker.distance < -200:
                R.kch.leds[UserLED.C] = Colour.RED
                R.kch.leds[UserLED.A] = Colour.OFF
                R.kch.leds[UserLED.B] = Colour.OFF
            
            else:
                R.kch.leds[UserLED.B] = Colour.RED
                R.kch.leds[UserLED.C] = Colour.OFF
                R.kch.leds[UserLED.A] = Colour.OFF
            
            time.sleep(0.5)
            
bulletPoint3()
