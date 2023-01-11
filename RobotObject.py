
from sr.robot3 import *
import time
import math

class robot:
    
    def __init__(self):
        self.R = Robot() 
        
        markers = self.R.camera.see_ids()
        
        #determines the starting corner of the robot based on placement of the robot and the defined orietnation based on the srategy
        if 14 in markers:
            self.starting_corner = 1
        elif 7 in markers:
            self.starting_corner = 0
        elif 0 in markers:
            self.starting_corner = 3
        elif 21 in markers:
            self.starting_corner = 2
    
    def moveDist(self, dist, speed=0.5):
        
        rotDist = 100 * math.pi
        self.R.ruggeduino.command("s")
        self.R.motor_board.motors[0].power = speed
        self.R.motor_board.motors[1].power = speed
        encLeft = self.R.ruggeduino.command("x")
        encRight = self.R.ruggeduino.command("y")
        while (encLeft + encRight)/2 < (dist/rotDist)*360:
            encLeft = self.R.ruggeduino.command("x")
            encRight = self.R.ruggeduino.command("y")
            time.sleep(0.005)
        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0 

    def faceDirection(self, direc, speed=0.5):
        
        #uses a 2D array to determine wall markers in each direction relative to a birds eye perspective 
        wallMarkers = [[0,1,2,3,4,5,6], [7,8,9,10,11,12,13], [14,15,16,17,18,19,20], [21,22,23,24,25,26,27]]
        direc = direc.lower()
        if direc == "north":
            usedMarkers = wallMarkers[0]
        elif direc == "south":
            usedMarkers = wallMarkers[2]
        elif direc == "east":
            usedMarkers = wallMarkers[1]
        elif direc == "west":
            usedMarkers = wallMarkers[3]
        
        markers = self.R.camera.see_ids()
        #creates an array of markers that the camera both sees and are on the correct wall realative to the robot 
        intersection = [marker for marker in markers if marker in usedMarkers]
        
        #rotates the robot until the above task is complete 
        while len(intersection) < 1:
            self.R.motor_board.motors[0].power = speed
            self.R.motor_board.motors[1].power = -speed
            time.sleep(0.1)
            self.R.motor_board.motors[0].power = 0
            self.R.motor_board.motors[1].power = 0
            markers = self.R.camera.see_ids()
            intersection = [marker for marker in markers if marker in usedMarkers]
        
        markersFull = self.R.camera.see()
        
        #creates a second list of full markers where only the markers that have been seen and are located on the correct wall are used 
        intersection2 = [marker for marker in markersFull if marker.id in usedMarkers]
        
        #checks for the angle to the wall within a 5 degree margin of error and turns to face that wall accordingly 
        while True:
            #loops through each value the set of markers seen and checks for perpendicularity 
            for i in intersection2:
                if i.orientation.rot_y * (180/math.pi) > -5 and i.orientation.rot_y * (180/math.pi) < 5:
                    break
            self.R.motor_board.motors[0].power = 0.2
            self.R.motor_board.motors[1].power = -0.2
            time.sleep(0.1)
            self.R.motor_board.motors[0].power = 0
            self.R.motor_board.motors[1].power = 0
            
            markersFull = self.R.camera.see()
            intersection2 = [marker for marker in markersFull if marker.id in usedMarkers]

    
    #functions for interacting with brainboard LEDs 
    def turnOnLED (self, name="A", colour="cyan"):
        if name == "A" and colour == "cyan":
            self.R.kch.leds[UserLED.A] = Colour.CYAN
        if name == "B" and colour == "cyan":
            self.R.kch.leds[UserLED.B] = Colour.CYAN
        if name == "C" and colour == "cyan":
            self.R.kch.leds[UserLED.C] = Colour.CYAN
        if name == "A" and colour == "cyan":
            self.R.kch.leds[UserLED.A] = Colour.RED
        if name == "B" and colour == "cyan":
            self.R.kch.leds[UserLED.B] = Colour.RED
        if name == "C" and colour == "cyan":
            self.R.kch.leds[UserLED.C] = Colour.RED
        
    def turnOffLED (self, name="A"):
        if name == "A" and colour == "cyan":
            self.R.kch.leds[UserLED.A] = Colour.OFF
        if name == "B" and colour == "cyan":
            self.R.kch.leds[UserLED.B] = Colour.OFF
        if name == "C" and colour == "cyan":
            self.R.kch.leds[UserLED.C] = Colour.OFF
    
    #to be added for a rotation function
    def rotate(self, degrees):
        pass
    
    def faceMarker(self, marker_id, speed=0.5):
        markers = self.R.camera.see_ids()
        
        #the robot will stop roating as soon it sees the correct marker in its peripheral 
        while marker_id not in markers:
            self.R.motor_board.motors[0].power = speed
            self.R.motor_board.motors[1].power = -speed
            time.sleep(0.1)
            self.R.motor_board.motors[0].power = 0
            self.R.motor_board.motors[1].power = 0
            markers = self.R.camera.see_ids()

        markers = self.R.camera.see()
        for marker in markers:
            if marker.id == marker_id:
                dist = marker.distance
        dist_diff = 1
        
        while dist_diff > 0:
            
            self.R.motor_board.motors[0].power = 0.2
            self.R.motor_board.motors[1].power = -0.2
            time.sleep(0.1)
            self.R.motor_board.motors[0].power = 0
            self.R.motor_board.motors[1].power = 0
            markers = self.R.camera.see()
            for marker in markers:
                if marker.id == marker_id:
                    dist2 = marker.distance
            dist_diff = dist - dist2 
            dist = dist2

        self.R.motor_board.motors[0].power = -0.2
        self.R.motor_board.motors[1].power = 0.2
        time.sleep(0.1)
        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0

    def goToMarker(self, marker_id, speed=0.5):
        self.faceMarker(marker_id)
        markers = self.R.camera.see()
        for marker in markers:
            if marker.id == marker_id:
                usedMarker = marker
        #adds 5cm buffer between robot and wall
        self.moveDist(usedMarker.distance-50, speed)