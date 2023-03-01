from sr.robot3 import *
import time
from opencv import cv2
import numpy as np

R = Robot()

while True:
    markers = R.camera.see()
    if len(markers) >0:
        frame = R.camera.capture
        image = cv2.imread(frame)
        original = image.copy()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower = np.array([22, 93, 0], dtype="uint8")
        upper = np.array([45, 255, 255], dtype="uint8")
        mask = cv2.inRange(image, lower, upper)
