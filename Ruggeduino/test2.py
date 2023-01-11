#from sr.robot3 import Robot as R
import moveFunctions as move
import time

n=1
while True:
    move.moveRot(n,1)
    time.sleep(5)
    n += 1