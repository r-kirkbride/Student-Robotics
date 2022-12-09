from sr.robot3 import *
import cv2
import numpy as np
import time
R = Robot()

while True:
    markers = R.camera.see()
    if len(markers)>0:
        frame = R.camera.capture()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_val = np.array([20, 100, 100])
        higher_val = np.array([30, 255, 255])
        mask = cv2.inRange(hsv, lower_val, higher_val)
        if np.sum(mask) > 0:
            R.kch.leds[UserLED.C] = Colour.RED
        else:
            R.kch.leds[UserLED.A] = Colour.CYAN
    
    time.sleep(2)
    R.kch.leds[UserLED.A] = Colour.OFF
    R.kch.leds[UserLED.C] = Colour.OFF