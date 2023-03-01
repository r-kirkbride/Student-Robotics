# Student-Robotics

Robot object documentation for general use

When writing code in robot.py, ensure that the following imports are present 

from sr.robot3 import *
from RobotObject import robot
import time
import math

initialise or create an instance of the robot object as R = robot() and do not capatilise the R in robot. 

To use methods type out R. and then the method name with brackets after. Inside the brackets you can send arguments which tells the robot exactly what to do. Some methods do not have arguments which means you can type them out without needing to pass in any data 

R has one attribute which is its starting corner which it figures out when the code is initially run. To get the starting corner you can print(R.starting_corner) as the value is stored in attribute R.starting_corner


## Methods to use:

### R.moveDist(distance, speed=0.5, braking = Flase)

Can take 3 arguments:
- dist - required - distance to move (can be negative to reverse).
- speed - defaults to 0.5 - maximum speed to run the motors at (should always be positive, but can be negative).
- braking - defaults to False - determines whether the motors are braked or coasted.

### R.turnOnLED(name="A", colour="cyan")

takes two arguments but when called without arguments defaults to turning LED a cyan. You can change it so that if you want LED B or C to turn on you can pass in the letters "B" or "C" and if you want the colour to be red not cyan you can pass it "red" as a second argument. Note that if you want LED A to turn red you will have to manually type in "A" as the first argument and then type in "red"

### R.turnOffLED(name="A")

takes one argument and turns off the selected LED, defaults to A if no LED is provided 

### R.faceDirection(direc, speed=0.5)

takes two arguments, a direction, ("north", "south", "east", "west") and a speed which defaults to 0.5. This rotates the robot until it is facing the desired wall. Direction of rotation can e changed by passing in a negative speed

### R.faceMarker(markerID, speed=0.5)

takes two arguments, a number for the marker id and a speed which defaults to 0.5. This rotates the robot until it is facing the specified marker that is passed in as best it can. 

### R.goToMarker(markerID, speed=0.5)

takes two arguments, a number for the marker id and a speed which defaults to 0.5. This rotates the robot until it is facing the specified marker, then moves in a straight line towards the marker until it is 5cm away 

### R.driveToMarker()

takes no arguments (will be changed once R.faceMarker() is improved). This is used to tell the robot when to stop in relation to a target marker or an obstacle, which is figured out by the method.
