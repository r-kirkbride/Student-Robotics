import math
import time
from sr.robot3 import *

R = Robot()

# Distance in millimetres, -1 <= speed <= 1
def moveDist(dist, speed):
    rotDist = 100 * math.pi
    R.ruggeduino.command("s")
    R.motor_board.motors[0].power = speed
    R.motor_board.motors[1].power = speed
    encLeft = R.ruggeduino.command("x")
    encRight = R.ruggeduino.command("y")
    while (encLeft + encRight)/2 < (dist/rotDist)*360:
        encLeft = R.ruggeduino.command("x")
        encRight = R.ruggeduino.command("y")
        time.sleep(0.005)
    R.motor_board.motors[0].power = 0
    R.motor_board.motors[1].power = 0
    
def moveRot(rot, speed):
    R.ruggeduino.command("s")
    R.motor_board.motors[0].power = speed
    R.motor_board.motors[1].power = speed
    encLeft = R.ruggeduino.command("x")
    encRight = R.ruggeduino.command("y")
    while (encLeft + encRight)/2 < rot*360:
        encLeft = R.ruggeduino.command("x")
        encRight = R.ruggeduino.command("y")
        time.sleep(0.005)
    R.motor_board.motors[0].power = 0
    R.motor_board.motors[1].power = 0

def moveDeg(deg, speed):
    R.ruggeduino.command("s")
    R.motor_board.motors[0].power = speed
    R.motor_board.motors[1].power = speed
    encLeft = R.ruggeduino.command("x")
    encRight = R.ruggeduino.command("y")
    while (encLeft + encRight)/2 < deg:
        encLeft = R.ruggeduino.command("x")
        encRight = R.ruggeduino.command("y")
        time.sleep(0.005)
    R.motor_board.motors[0].power = 0
    R.motor_board.motors[1].power = 0