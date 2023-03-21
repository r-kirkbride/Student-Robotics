from robotObject import robot
from sr.robot3 import *
import time
R = robot()

#R.turnDeg(90) - we can choose start orientation so this is not required.

while True:
    R.goToMarker(73)
    R.grabToken()
    R.turnDeg(-180)
    R.moveDist(1000)
    R.goHome()
    R.releaseToken()
    R.rotateDeg(180)
    R.goAdjacent()
