#movement challenge

from sr.robot3 import *
#from moveDistance import moveDist
import time
import math

metreTimeTaken = 1

##Autonomously complete 3 continuous circuits of a triangular path, returning to its starting position to within 300mm.
##The path must be a isosceles right-angled triangle with shorter side length 1500 ±200mm.
##The direction of travel around the triangle and orientation of the robot are inconsequential.

R = Robot()

def move(dist):
    if dist < 0:
        R.motor_board.motors[0].power = -0.5
        R.motor_board.motors[1].power = -0.5
        time.sleep(metreTimeTaken * dist)
        R.motor_board.motors[0].power = 0
        R.motor_board.motors[1].power = 0
        time.sleep(0.5)
    elif dist > 0:
        R.motor_board.motors[0].power = 0.5
        R.motor_board.motors[1].power = 0.5
        time.sleep(metreTimeTaken * dist)
        R.motor_board.motors[0].power = 0
        R.motor_board.motors[1].power = 0
        time.sleep(0.5)

def triangularMovement():
    #moveDist(1500)
    move(1.5)
    R.motor_board.motors[0].power = -0.5
    R.motor_board.motors[1].power = 0.5
    time.sleep(0.35)
    R.motor_board.motors[0].power = 0
    R.motor_board.motors[1].power = 0
    time.sleep(0.5)
    move(1.5)
    R.motor_board.motors[0].power = -0.5
    R.motor_board.motors[1].power = 0.5
    time.sleep(0.85)
    R.motor_board.motors[0].power = 0
    R.motor_board.motors[1].power = 0
    time.sleep(0.5)
    move(2.1)
    R.motor_board.motors[0].power = -0.5
    R.motor_board.motors[1].power = 0.5
    time.sleep(0.85)
    R.motor_board.motors[0].power = 0
    R.motor_board.motors[1].power = 0
    time.sleep(0.5)

time.sleep(3)

for i in range(3):
    triangularMovement()
