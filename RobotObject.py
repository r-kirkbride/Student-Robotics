from sr.robot3 import *
import time
import math

class robot:
    
    def __init__(self):
        
        #Creates an instance of the robot object from sr.robot3 and saves it as in attribute to the instance of this class
        self.R = Robot() 
        
        markers = self.R.camera.see_ids()
        
        self.R.ruggeduino.command("s") #reset motor encoders
        
        
        self.R.ruggeduino.command("g")

        self.R.ruggeduino.command("d")
        time.sleep(0.5)
        self.R.ruggeduino.command("e")
        #determines the starting corner of the robot 
        #This because a each of the following markers IDs: 0, 7, 14, 21 is in each of the 4 corners
        """if 14 in markers:
            self.starting_corner = 1
        elif 7 in markers:
            self.starting_corner = 0
        elif 0 in markers:
            self.starting_corner = 3
        elif 21 in markers:
            self.starting_corner = 2"""
        
        #Deploys arms to the correct position upon initialising the robot 
        """self.R.servo_board.servos[1].position = 0.8
        self.R.servo_board.servos[2].position = -0.8"""

    """def moveDist(self, dist, speed=0.5):
        
        #speed defaults to 0.5 so it doesn't need to be passed
        rotDist = 100 * math.pi #circumference of the wheel in mm
        degrees = (dist/rotDist) * 360 #number of degrees to rotate
        self.R.ruggeduino.command("s") #reset motor encoders
        self.R.motor_board.motors[0].power = speed
        self.R.motor_board.motors[1].power = speed
        encLeft = int(self.R.ruggeduino.command("x"))
        encRight = int(self.R.ruggeduino.command("y"))
        while (encLeft + encRight)/2 < degrees:
            encLeft = int(self.R.ruggeduino.command("x"))
            encRight = int(self.R.ruggeduino.command("y"))
            time.sleep(0.005)
        while encLeft > degrees and encRight < degrees:
            self.R.motor_board.motors[0].power = speed
            self.R.motor_board.motors[1].power = -speed
            time.sleep(0.005)
        while encLeft < degrees and encRight > degrees:
            self.R.motor_board.motors[0].power = -speed
            self.R.motor_board.motors[1].power = speed
            time.sleep(0.005)
        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0""" 

    # Distance in millimetres, -1 <= speed <= 1
    def moveDist(self, dist, speed=0.5,braking = True):
        CIRCUMFERENCE = 100 * math.pi #circumference of the wheels
        TOLERANCE = 5 #tolerance of difference before it compensates
        degreesPerRot = 80
        degrees = (dist/CIRCUMFERENCE)*degreesPerRot #number of degrees to rotate
        reverseMultiplier = speed/abs(speed) #will be -1 if robot is going to reverse, otherwise 1
        if dist < 0:
            return self.moveDist(abs(dist),-speed,braking)
        self.R.ruggeduino.command("s")
        self.R.motor_board.motors[0].power = speed
        self.R.motor_board.motors[1].power = speed
        encLeft = int(self.R.ruggeduino.command("x"))
        encRight = int(self.R.ruggeduino.command("y"))
        while (encLeft + encRight)/2 < degrees:
            #print(f"L:{encLeft}, {self.R.motor_board.motors[0].power}\tR:{encRight}, {self.R.motor_board.motors[1].power}")
            encLeft = int(self.R.ruggeduino.command("x"))
            encRight = int(self.R.ruggeduino.command("y"))
            if encLeft > encRight + TOLERANCE:
                self.R.motor_board.motors[0].power -= reverseMultiplier * 0.005
            elif encRight > encLeft + TOLERANCE:
                self.R.motor_board.motors[1].power -= reverseMultiplier * 0.005
            else:
                self.R.motor_board.motors[0].power = speed
                self.R.motor_board.motors[1].power = speed
            time.sleep(0.05)
        if braking:
            self.R.motor_board.motors[0].power = -1*reverseMultiplier
            self.R.motor_board.motors[1].power = -1*reverseMultiplier
            while int(self.R.ruggeduino.command("x")) > 5 and int(self.R.ruggeduino.command("y")) > 5:
                self.R.ruggeduino.command("s")
                time.sleep(0.005)
        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0

    """def rotateDeg(self, deg, speed=0.5):
        rotDist = 100 * math.pi
        degrees = (((deg/360)*400*math.pi)/rotDist)*360
        if dist > 0:
            leftSpeed, rightSpeed = speed, -speed
        else:
            leftSpeed, rightSpeed = speed, -speed
        self.R.ruggeduino.command("s")
        self.R.motor_board.motors[0].power = leftSpeed
        self.R.motor_board.motors[1].power = rightSpeed
        encLeft = int(self.R.ruggeduino.command("x"))
        encRight = int(self.R.ruggeduino.command("y"))
        while (encLeft + encRight)/2 < degrees:
            encLeft = int(self.R.ruggeduino.command("x"))
            encRight = int(self.R.ruggeduino.command("y"))
            if encLeft > encRight:
                self.R.motor_board.motors[0].power = leftSpeed - 0.025
            elif encRight > encLeft:
                self.R.motor_board.motors[1].power = rightSpeed + 0.025
            time.sleep(0.05)
        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0"""
        
    """def moveRot(self, rot, speed=0.5):
        R.ruggeduino.command("s")
        R.motor_board.motors[0].power = speed
        R.motor_board.motors[1].power = speed
        encLeft = int(self.R.ruggeduino.command("x"))
        encRight = int(self.R.ruggeduino.command("y"))
        while (encLeft + encRight)/2 < rot*360:
            encLeft = int(self.R.ruggeduino.command("x"))
            encRight = int(self.R.ruggeduino.command("y"))
            time.sleep(0.005)
        R.motor_board.motors[0].power = 0
        R.motor_board.motors[1].power = 0
    def moveDeg(self, deg, speed=0.5):
        R.ruggeduino.command("s")
        R.motor_board.motors[0].power = speed
        R.motor_board.motors[1].power = speed
        encLeft = int(self.R.ruggeduino.command("x"))
        encRight = int(self.R.ruggeduino.command("y"))
        while (encLeft + encRight)/2 < deg:
            encLeft = int(self.R.ruggeduino.command("x"))
            encRight = int(self.R.ruggeduino.command("y"))
            time.sleep(0.005)
        R.motor_board.motors[0].power = 0
        R.motor_board.motors[1].power = 0"""

    def drive(self, times = 0.5):
        self.R.motor_board.motors[0].power = 0.5
        self.R.motor_board.motors[1].power = 0.5
        time.sleep(times)
        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0

    def faceDirection(self, direc, speed=0.5):
        
        #this method is used for turning the robot to face one of the 4 walls 
        #uses a 2D array to determine wall markers in each direction relative to a birds eye perspective 
        wallMarkers = [[0,1,2,3,4,5,6], [7,8,9,10,11,12,13], [14,15,16,17,18,19,20], [21,22,23,24,25,26,27]]
        #input sanitation 
        direc = direc.lower()
        #chooses the used markers based on input given
        if direc == "north":
            usedMarkers = wallMarkers[0]
        elif direc == "south":
            usedMarkers = wallMarkers[2]
        elif direc == "east":
            usedMarkers = wallMarkers[1]
        elif direc == "west":
            usedMarkers = wallMarkers[3]
        
        markers = self.R.camera.see_ids()
        #creates an array of markers that the camera both sees and are on the correct wall relative to the robot 
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
        Facing = False
        while not Facing:
            #loops through each value the set of markers seen and checks for perpendicularity 
            for i in intersection2:
                if i.orientation.rot_y * (180/math.pi) > -5 and i.orientation.rot_y * (180/math.pi) < 5:
                    Facing = True
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
        if name == "A":
            self.R.kch.leds[UserLED.A] = Colour.OFF
        if name == "B":
            self.R.kch.leds[UserLED.B] = Colour.OFF
        if name == "C":
            self.R.kch.leds[UserLED.C] = Colour.OFF
    
    #to be added for a rotation function
    def rotate(self, degrees):
        pass
    
    def grabToken(self):
        self.moveDist(600)
        self.R.ruggeduino.command("c")
        time.sleep(0.5)
        self.R.ruggeduino.command("b")
    
    def faceMarker(self, marker_id):
        flag = False
        
        distance = 9999999999
        counting = 0
        while counting < 18:
            self.R.motor_board.motors[0].power = -0.3
            self.R.motor_board.motors[1].power = 0.3
            time.sleep(0.5)
            self.R.motor_board.motors[0].power = 0
            self.R.motor_board.motors[1].power = 0
            time.sleep(0.3)
            markers = self.R.camera.see()
            for i in range(len(markers)):
                if markers[i].id == marker_id:
                    distance = markers[i].distance
                    print("honed in")
                    #print(f"distance: {distance}")

                    #self.lookAtMarker(marker_id)
                    flag = True
                    break
            
            if flag == True:
                break

            counting += 1
        
        #if counting >= 18:
            #print(f"Error in first stage of face new marker")


        flag = False
        count = 0
        
        while count < 30:

            self.R.motor_board.motors[0].power = -0.2
            self.R.motor_board.motors[1].power = 0.2
            time.sleep(0.2)
            self.R.motor_board.motors[0].power = 0
            self.R.motor_board.motors[1].power = 0
            time.sleep(0.3)
            markers = self.R.camera.see()
            for i in range(len(markers)):
                    if markers[i].id == marker_id:
                        tempDistance = markers[i].distance
                        #print(f"new distance: {tempDistance}")
                        if tempDistance > distance or abs(tempDistance - distance) < 2.5:
                            print("facing")
                            #if abs(tempDistance - distance) < 2.5:
                                #print("tolerance was done")
                            flag = True
                            break
                        else:
                            distance = tempDistance
            
            if flag == True:
                break
            
            count += 1
        
            
        #self.R.motor_board.motors[0].power = 0.2
        #self.R.motor_board.motors[1].power = -0.2
        #self.R.sleep(0.1)
        #self.R.motor_board.motors[0].power = 0
        #self.R.motor_board.motors[1].power = 0
        time.sleep(0.1)

        if count >= 30:
            print("Error in the second in the second stage in the new marker")
            #print("has turned too much")
            #in case stuck
            self.R.motor_board.motors[0].power = -0.5
            self.R.motor_board.motors[1].power = -0.5
            time.sleep(0.2)
            self.R.motor_board.motors[0].power = 0
            self.R.motor_board.motors[1].power = 0
            #print("stuck")
            return


    def goToMarker(self, marker_id, speed=0.5):
        self.faceMarker(marker_id)
        markers = self.R.camera.see()
        usedMarker = 934000
        for marker in markers:
            if marker.id == marker_id:
                usedMarker = marker
        if usedMarker == 934000:
            return "Marker not seen"
        else:
            print(f"used marker id: {usedMarker.id}")
            #adds 50mm buffer between robot and object
            counter = 0 
            while usedMarker.distance > 50:
                angle = usedMarker.spherical.rot_y
                self.drive(times = 0.5)
                markers = self.R.camera.see()
                marker_ids = []
                for m in markers:
                    marker_ids.append(m.id)
                    if m.id == usedMarker.id:
                        angle = m.spherical.rot_y
                print(f"marker ids: {marker_ids}")
                if angle > 0:
                    speed = -0.15
                else:
                    speed = 0.15
                print(angle)
                print(speed)
                if abs(angle) > 0.1:
                    self.R.motor_board.motors[0].power = speed
                    self.R.motor_board.motors[1].power = -speed
                    time.sleep(0.4)
                    self.R.motor_board.motors[0].power = 0
                    self.R.motor_board.motors[1].power = 0
                    print("corrected")
                if usedMarker.id in marker_ids:
                    pass
                else:
                    print("cant see marker")
                    break

                #if counter == 4:
                    #markers = self.R.camera.see()
                    # usedMarker in markers:
                        #if abs(usedMarker.spherical.rot_y) > 0.5:
                            #self.faceMarker(marker_id)
                        #counter = 0 
                #counter+=1
        
        print("donee")
    
    #drives to marker until close enough
    def driveToMarker(self):

        #hard coded testing for the method, can be removed once goToMarker is accurate
        self.R.motor_board.motors[1].power = 0.5
        self.time.sleep(0.28)       
        self.R.motor_board.motors[0].power = 0.5

        #to see if the robot is close enough to the marker or any obstacles, breaks out of loop once that is the case
        going = True
        while going:
            going = self.checkMarker()
            self.time.sleep(0.1)
        
        #stops to robot
        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0

    #method that checks distance of obstacle to robot
    def checkMarker(self):

        going = True

        #checks whether closest thing is a marker or an obstacle and sets the distance to stop accordingly
        markers = self.R.camera.see()
        if markers[0].id > 27:
            toStop = 0.3
        else:
            toStop = 0.5

        #checks the distance of the nearest object to the robot
        frontDistance = self.R.ruggeduino.pins[A4].analogue_read()
        frontLeft = self.R.ruggeduino.pins[A0].analogue_read()
        frontRight = self.R.ruggeduino.pins[A1].analogue_read()


        #if distance to object is less than a certain distance, the method tells robot to stop through the return
        if frontDistance < toStop or frontLeft < toStop - 0.2 or frontRight < toStop - 0.2:
            going = False
        
        return going
    def setPos(self):
        self.R.servo_board.servos[0].position=0
        time.sleep(0.2)
        self.R.servo_board.servos[2].position=0
    
    #Reverses 0.5m and rotates 90 degrees
    def escape(self):
        markers = self.R.camera.see_ids()
        if len(markers) == 0:
            moveDist(500, -0.3)
            R.motor_board.motors[0].power = -0.5
            R.motor_board.motors[1].power = 0.5
            time.sleep(0.2)
            R.motor_board.motors[0].power = 0
            R.motor_board.motors[1].power = 0
