


from sr.robot3 import *
import time
import math

class robot:
    
    def __init__(self):
        
        #Creates an instance of the robot object from sr.robot3 and saves it as in attribute to the instance of this class
        self.R = Robot() 
        
        markers = self.R.camera.see_ids()

        corner0 = [24,25,26,27,0,1,2]
        corner1 = [3,4,5,6,7,8,9]
        corner2 = [10,11,12,13,14,15,16]
        corner3 = [17,18,19,20,21,22,23]
        self.middleMarkers = [3,10,17,24]
        self.cornerNum = 0
        self.wallMarkers = [corner0, corner1, corner2, corner3]
        self.wallThings = [[0,1,2,3,4,5,6], [7,8,9,10,11,12,13], [14,15,16,17,18,19,20], [21,22,23,24,25,26,27]]
       
        #Deploys arms to the correct position upon initialising the robot 
        #self.R.servo_board.servos[1].position = 0.8
        #self.R.servo_board.servos[2].position = -0.8
    def move(self):
        self.R.motor_board.motors[0].power = 0.5
        self.R.motor_board.motors[1].power = 0.5
        self.R.sleep(0.5)
        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0
        
    def spin(self):
        self.R.motor_board.motors[0].power = 0.5
        self.R.motor_board.motors[1].power = -0.5
        self.R.sleep(0.5)
        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0
    
    def checkCollisons(self):
        collided = False
        if (self.R.ruggeduino.pins[A0].analogue_read() < 0.5 or self.R.ruggeduino.pins[A0].analogue_read() < 0.5) and ((self.R.ruggeduino.pins[A4].analogue_read() > 0) and (self.R.ruggeduino.pins[A4].analogue_read() < 0.17)):
            collided = True
        return collided 
    
    def findStartingCorner(self):
        self.spin()
        markers = self.R.camera.see()
        mini = markers[0]
        if mini.id in self.wallMarkers[0]:
            self.starting_corner = 0
        elif mini.id in self.wallMarkers[1]:
            self.starting_corner = 1
        elif mini.id in self.wallMarkers[2]:
            self.starting_corner = 2
        elif mini.id in self.wallMarkers[3]:
            self.starting_corner = 3
        
    
    def moveDist(self, dist, speed=0.5):
        
        #speed defaults to 0.5 so it doesn't need to be passed
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
        
        #this method is used for turning the robot to face one of the 4 walls 
        #uses a 2D array to determine wall markers in each direction relative to a birds eye perspective 
        
        #input sanitation 
        self.direction = direc
        #chooses the used markers based on input given
        if direc == "north":
            usedMarkers = self.wallThings[self.cornerNum % 4]
        elif direc == "south":
            usedMarkers = self.wallThings[(self.cornerNum+2) % 4]
        elif direc == "east":
            usedMarkers = self.wallThings[(self.cornerNum+1) % 4]
        elif direc == "west":
            usedMarkers = self.wallThings[(self.cornerNum+3) % 4]
        
        markers = self.R.camera.see_ids()
        
        #creates an array of markers that the camera both sees and are on the correct wall relative to the robot 
        intersection = [marker for marker in markers if marker in usedMarkers]
        
        #rotates the robot until the above task is complete 
        while len(intersection) < 1:
            self.R.motor_board.motors[0].power = speed
            self.R.motor_board.motors[1].power = -speed
            self.R.sleep(0.1)
            self.R.motor_board.motors[0].power = 0
            self.R.motor_board.motors[1].power = 0
            markers = self.R.camera.see_ids()
            intersection = [marker for marker in markers if marker in usedMarkers]
        
        
        
    
        markers = self.R.camera.see()
        
       
        #creates a second list of full markers where only the markers that have been seen and are located on the correct wall are used 
        markers = [marker for marker in markers if marker.id in usedMarkers]
        
        
        #checks for the angle to the wall within a 5 degree margin of error and turns to face that wall accordingly 
        if len(markers) == 0:
            self.faceDirection(direc)
        else:
            answer = abs(abs(markers[0].orientation.rot_y) - abs(markers[0].spherical.rot_y))
            answer1=999999999
            tututu = abs(markers[0].orientation.rot_y)
            turned = False
            while answer > 0.07:
                self.R.motor_board.motors[0].power = speed/10
                self.R.motor_board.motors[1].power = -speed/10
                self.R.sleep(0.1)
                self.R.motor_board.motors[0].power = 0
                self.R.motor_board.motors[1].power = 0
                markers = self.R.camera.see()
                markers = [marker for marker in markers if marker.id in usedMarkers]
                if tututu > answer1 and not turned :
                    speed = -speed
                    turned = True
                answer1 = tututu
                
                if len(markers)==0:
                    break
                tututu = abs(abs(markers[0].orientation.rot_y)) 
                answer = abs(abs(markers[0].orientation.rot_y) - abs(markers[0].spherical.rot_y))
                
            
            self.R.motor_board.motors[0].power = 0.05
            self.R.motor_board.motors[1].power = -0.05
            self.R.sleep(0.1)
            self.R.motor_board.motors[0].power = 0
            self.R.motor_board.motors[1].power = 0
        
        self.R.sleep(1)
      
      
            
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
            self.R.motor_board.motors[0].power = 0.5
            self.R.motor_board.motors[1].power = -0.5
            self.R.sleep(0.1)
            self.R.motor_board.motors[0].power = 0
            self.R.motor_board.motors[1].power = 0
            markers = self.R.camera.see_ids()

        #sets up the initial distance as it compares the distance to the marker to previous distances  
        markers = self.R.camera.see()
        dist = 0
        for marker in markers:
            if marker.id == marker_id:
                dist = marker.distance
        dist_diff = 1
        dist2=99999999
        while dist < dist2:
            
            dist2 = dist
            self.R.motor_board.motors[0].power = 0.1
            self.R.motor_board.motors[1].power = -0.1
            time.sleep(0.1)
            self.R.motor_board.motors[0].power = 0
            self.R.motor_board.motors[1].power = 0
            markers = self.R.camera.see()
            if len(markers) > 0:
                for marker in markers:
                    if marker.id == marker_id:
                        dist = marker.distance
                 
                
            else:
                break 

        self.R.motor_board.motors[0].power = -0.1
        self.R.motor_board.motors[1].power = 0.1
        time.sleep(0.1)
        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0
    
    def lookAtMarker(self, marker_id, counter = 1):
        marker_ids = []
        markers = self.R.camera.see()
        for i in range(len(markers)):
            marker_ids.append(markers[i].id)

        if len(markers) > 0:
            idx = 0 
            minDist = 9000000000

            for i in range(counter):
                self.R.motor_board.motors[0].power = -0.08
                self.R.motor_board.motors[1].power = 0.08
                self.R.sleep(0.5)
                self.R.motor_board.motors[0].power = 0
                self.R.motor_board.motors[1].power = 0
            for i in range(2*counter):
                if len(markers) > 0:
                    self.R.motor_board.motors[0].power = 0.08
                    self.R.motor_board.motors[1].power = -0.08
                    self.R.sleep(0.5)
                    self.R.motor_board.motors[0].power = 0
                    self.R.motor_board.motors[1].power = 0
                    #intersection1 = [marker for marker in markers if marker.id<28]
                    #intersection = [marker for marker in intersection1 if marker not in self.wallMarkers[self.cornerNum %4]]
                    #print(intersection)

                    for i in range(len(marker_ids)):
                        if marker_id == marker_ids[i]:

                            if markers[i].distance < minDist:
                                idx = i
                                minDist = markers[i].distance
                                print(idx) 
                    #for marker in markers:
                        #if marker.id > 27:
                            #if marker.distance < minDist:
                                #print(marker.distance, marker.id)
                                #idx = i 
                    marker_ids = []
                    markers = self.R.camera.see()
                    for i in range(len(markers)):
                        marker_ids.append(markers[i].id)
                else:
                    self.lookAtMarker(marker_id,counter+3)
            for i in range((2*counter)-idx):
                self.R.motor_board.motors[0].power = -0.08
                self.R.motor_board.motors[1].power = 0.08
                self.R.sleep(0.5)
                self.R.motor_board.motors[0].power = 0
                self.R.motor_board.motors[1].power = 0
            
            if idx == 0:
                self.lookAtMarker(marker_id,counter+1)
            marker_ids = []
            markers = self.R.camera.see()
            for i in range(len(markers)):
                marker_ids.append(markers[i].id)
            #markers = [marker for marker in markers if marker.id > 27]
            for i in range(len(marker_ids)):
                if marker_id == marker_ids[i]:


                    usedAngle = markers[i].spherical.rot_y
                    if usedAngle < 0:
                        speed = -0.01
                    else:
                        speed = 0.01 
                    minAngle = 999090909

                    for j in range(len(marker_ids)):
                        if marker_id == marker_ids[j]:

                            while abs(markers[j].spherical.rot_y) <= minAngle:
                                self.R.motor_board.motors[0].power = speed
                                self.R.motor_board.motors[1].power = -speed
                                self.R.sleep(0.5)
                                self.R.motor_board.motors[0].power = 0
                                self.R.motor_board.motors[1].power = 0
                                if abs(markers[j].spherical.rot_y) < minAngle:
                                    minAngle = abs(markers[j].spherical.rot_y)
                                marker_ids = []
                                markers = self.R.camera.see()
                                for i in range(len(markers)):
                                    marker_ids.append(markers[i].id)
                                print(f"markers that can be seen {markers}")
                                print(f"markers IDS that can be seen {markers_ids}")
                                #markers = [marker for marker in markers if marker.id > 27]
                        



                    self.R.motor_board.motors[0].power = -speed
                    self.R.motor_board.motors[1].power = speed
                    self.R.sleep(0.5)
                    self.R.motor_board.motors[0].power = 0
                    self.R.motor_board.motors[1].power = 0
                else:
                    self.lookAtMarker(marker_id,counter+1)
    
    def newFaceMarker(self, marker_id):
        flag = False
        

        for i in range(18):
            self.R.motor_board.motors[0].power = -0.2
            self.R.motor_board.motors[1].power = 0.2
            self.R.sleep(0.15)
            self.R.motor_board.motors[0].power = 0
            self.R.motor_board.motors[1].power = 0
            self.R.sleep(0.1)
            markers = self.R.camera.see()
            for i in range(len(markers)):
                if markers[i].id == marker_id:
                    distance = markers[i].distance
                    print("honed in")
                    print(f"distance: {distance}")

                    #self.lookAtMarker(marker_id)
                    flag = True
                    break
            
            if flag == True:
                break


        flag = False
        
        while True:

            self.R.motor_board.motors[0].power = -0.2
            self.R.motor_board.motors[1].power = 0.2
            self.R.sleep(0.05)
            self.R.motor_board.motors[0].power = 0
            self.R.motor_board.motors[1].power = 0
            self.R.sleep(0.1)
            markers = self.R.camera.see()
            for i in range(len(markers)):
                    if markers[i].id == marker_id:
                        tempDistance = markers[i].distance
                        print(f"new distance: {tempDistance}")
                        if tempDistance > distance:
                            flag = True
                            break
                        else:
                            distance = tempDistance
            
            if flag == True:
                break
            
        self.R.motor_board.motors[0].power = 0.2
        self.R.motor_board.motors[1].power = -0.2
        self.R.sleep(0.1)
        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0
        self.R.sleep(0.1)

        markers = self.R.camera.see()
        for i in range(len(markers)):
                if markers[i].id == marker_id:
                    tempDistance = markers[i].distance
                    print(f"final distance: {tempDistance}")
                    break


        








    

    def goToMarker(self, marker_id, speed=0.5):
        self.faceMarker(marker_id)
        markers = self.R.camera.see()
        for marker in markers:
            if marker.id == marker_id:
                usedMarker = marker
        #adds 5cm buffer between robot and wall
        while usedMarker.distance > 50 and not self.checkCollisons() :
            print(self.R.ruggeduino.pins[A0].analogue_read())
            self.R.motor_board.motors[0].power = 0.5
            self.R.motor_board.motors[1].power = 0.5
            self.R.sleep(0.5)
            self.R.motor_board.motors[0].power = 0
            self.R.motor_board.motors[1].power = 0
    
    def goHome(self):
        markers = self.R.camera.see_ids()
        intersection = [marker for marker in markers if marker in self.wallMarkers[self.starting_corner][:len(self.wallMarkers[self.starting_corner])//2]]
        while len(intersection) < 1:
            self.spin()
            markers = self.R.camera.see_ids()
            intersection = [marker for marker in markers if marker in self.wallMarkers[self.starting_corner][:len(self.wallMarkers[self.starting_corner])//2]]
        self.goToMarker(intersection[0])
    
    def grabBoxes(self):
        self.R.motor_board.motors[0].power = -0.25
        self.R.motor_board.motors[1].power = 0.25
        self.R.sleep(0.5)
        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0
        markers = self.R.camera.see()
        for marker in markers:
            if marker.id > 27:
                print(marker.distance)
                print(marker.id)
                self.goToMarker(marker.id)
                if self.R.ruggeduino.pins[A4].analogue_read() > 1:
                    print(self.R.ruggeduino.pins[A4].analogue_read())
                    self.R.servo_board.servos[1].position = 0
                    while not self.R.ruggeduino.pins[2].digital_read():
                        self.R.motor_board.motors[0].power = -0.5
                        self.R.motor_board.motors[1].power = -0.5
                        self.R.sleep(0.5)
                        self.R.motor_board.motors[0].power = 0
                        self.R.motor_board.motors[1].power = 0
                    self.R.servo_board.servos[0].position = 1
    
    #drives to marker until close enough
    def driveToMarker(self, marker):

        #hard coded testing for the method, can be removed once goToMarker is accurate
        
        self.R.faceMarker(marker)
        self.R.motor_board.motors[1].power = 0.5
        self.R.sleep(0.28)       
        self.R.motor_board.motors[0].power = 0.5

        #to see if the robot is close enough to the marker or any obstacles, breaks out of loop once that is the case
        going = True
        while going:
            going = self.checkMarker()
            self.R.sleep(0.1)
        
        #stops to robot
        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0

    #method that checks distance of obstacle to robot
    def checkMarker(self, toStop=0.6):

        going = True

        #checks whether closest thing is a marker or an obstacle and sets the distance to stop accordingly
        markers = self.R.camera.see()
        if len(markers) != 0:
            if markers[0].id > 27:
                toStop = 0.2
                self.nearToken = True
            

            #checks the distance of the nearest object to the robot
            frontDistance = self.R.ruggeduino.pins[A4].analogue_read()
            frontLeft = self.R.ruggeduino.pins[A0].analogue_read()
            frontRight = self.R.ruggeduino.pins[A1].analogue_read()


            #if distance to object is less than a certain distance, the method tells robot to stop through the return
            if frontDistance < toStop or frontLeft < toStop - 0.2 or frontRight < toStop - 0.2:
                going = False
            
        return going
    
    def checkWall(self):
        going = True 
        frontDistance = self.R.ruggeduino.pins[A4].analogue_read()
        frontLeft = self.R.ruggeduino.pins[A0].analogue_read()
        frontRight = self.R.ruggeduino.pins[A1].analogue_read()

        if frontDistance < 0.5 and frontLeft <0.3 and frontRight < 0.3:
            print(frontDistance, frontLeft,frontRight)
            going = False
        
        return going

    def checkGoing(self):
        self.R.motor_board.motors[0].power = -0.5
        self.R.motor_board.motors[1].power = 0.5
        self.R.sleep(0.3)
        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0
        going = self.checkWall()
        while going:
            self.move()
            going = self.checkWall()

    def faceClosestToken(self, counter):
        markers = self.R.camera.see()
        if len(markers) > 0:
            idx = 0 
            minDist = 9000000000

            for i in range(counter):
                self.R.motor_board.motors[0].power = -0.08
                self.R.motor_board.motors[1].power = 0.08
                self.R.sleep(0.5)
                self.R.motor_board.motors[0].power = 0
                self.R.motor_board.motors[1].power = 0
            for i in range(2*counter):
                if len(markers) > 0:
                    self.R.motor_board.motors[0].power = 0.08
                    self.R.motor_board.motors[1].power = -0.08
                    self.R.sleep(0.5)
                    self.R.motor_board.motors[0].power = 0
                    self.R.motor_board.motors[1].power = 0
                    #intersection1 = [marker for marker in markers if marker.id<28]
                    #intersection = [marker for marker in intersection1 if marker not in self.wallMarkers[self.cornerNum %4]]
                    #print(intersection)
                    if markers[0].distance < minDist and markers[0].id > 27 :
                        idx = i
                        minDist = markers[0].distance
                        print(idx) 
                    #for marker in markers:
                        #if marker.id > 27:
                            #if marker.distance < minDist:
                                #print(marker.distance, marker.id)
                                #idx = i 
                    markers = self.R.camera.see()
                else:
                    self.faceClosestToken(counter+3)
            for i in range((2*counter)-idx):
                self.R.motor_board.motors[0].power = -0.08
                self.R.motor_board.motors[1].power = 0.08
                self.R.sleep(0.5)
                self.R.motor_board.motors[0].power = 0
                self.R.motor_board.motors[1].power = 0
            
            if idx == 0:
                self.faceClosestToken(counter+1)
            markers = self.R.camera.see()
            markers = [marker for marker in markers if marker.id > 27]
            if len(markers) > 0:
                usedAngle = markers[0].spherical.rot_y
                if usedAngle < 0:
                    speed = -0.01
                else:
                    speed = 0.01 
                minAngle = 999090909
                while abs(markers[0].spherical.rot_y) <= minAngle:
                    self.R.motor_board.motors[0].power = speed
                    self.R.motor_board.motors[1].power = -speed
                    self.R.sleep(0.5)
                    self.R.motor_board.motors[0].power = 0
                    self.R.motor_board.motors[1].power = 0
                    if abs(markers[0].spherical.rot_y) < minAngle:
                        minAngle = abs(markers[0].spherical.rot_y)
                    markers = self.R.camera.see()
                    markers = [marker for marker in markers if marker.id > 27]
                self.R.motor_board.motors[0].power = -speed
                self.R.motor_board.motors[1].power = speed
                self.R.sleep(0.5)
                self.R.motor_board.motors[0].power = 0
                self.R.motor_board.motors[1].power = 0
            else:
                self.faceClosestToken(counter+1)


    def getAngles(self):
        markers = self.R.camera.see()
        for marker in markers:
            print(marker.spherical.rot_y)
    
    def searchForWalls(self):
        fullMarkers = []
        for i in range(9):
            self.R.motor_board.motors[0].power = -0.2
            self.R.motor_board.motors[1].power = 0.2
            self.R.sleep(0.3)
            self.R.motor_board.motors[0].power = 0
            self.R.motor_board.motors[1].power = 0
            markers = self.R.camera.see()
            markers = [marker for marker in markers if marker.id < 28]
            for marker in markers:
                if marker in fullMarkers:
                    markers.remove(marker)
            fullMarkers += markers
        markers = sorted(fullMarkers, key=lambda x: x.distance)
    
        return markers
    
    def findClosestCornerMarker(self, x):

        n = 0
        
        fullMarkers = self.searchForWalls()
        self.R.sleep(0.1)
        print((f"All the wall markers it can see: {fullMarkers}"))
        print(f"This is cloest wall marker: {fullMarkers[0]}")

        for i in range(len(self.wallMarkers)):
            if fullMarkers[0].id in self.wallMarkers[i]:
                print(f"This is i :{i}")
                n = i
                print(f"This is n :{i}")
                break

        wanted = self.wallMarkers[(self.cornerNum + n + x ) % 4]

        print(f"This is wanted :{wanted}")

        targetMarker = None

        for i in range(len(fullMarkers)):
            if fullMarkers[i].id in wanted:
                targetMarker = fullMarkers[i]
                break
        return targetMarker
    
    def findClosestHomeMarker(self):

        fullMarkers = self.searchForWalls()
        print((fullMarkers))
        wantedHome = self.wallMarkers[(self.cornerNum ) % 4]
        targetMarker = None

        for i in range(len(fullMarkers)):
            if fullMarkers[i].id in wantedHome:
                targetMarker = fullMarkers[i]
                break
        return targetMarker




    

    def getBox(self):

        while True:

            if not self.facingCorner(1):
                self.faceMarker(self.markerToFace)
            self.faceClosestToken(3)
            going = self.checkMarker()
            idx = 0 
            while going:
                self.R.motor_board.motors[0].power = 0.3
                self.R.motor_board.motors[1].power = 0.3
                self.R.sleep(0.2)
                self.R.motor_board.motors[0].power = 0
                self.R.motor_board.motors[1].power = 0
                going = self.checkMarker()

            self.R.servo_board.servos[0].position = 0.7
            self.R.servo_board.servos[1].position = 0.7
            self.R.sleep(0.3)
            
            markers = self.searchForWalls()
            while len(markers) == 0:
                going = self.checkWall()
                if going:
                    self.move()
                    markers = self.searchForWalls()
                else:
                    self.escape()
                    markers = self.searchForWalls()
            
                
            if markers[0].id in self.wallThings[0]:
                self.faceDirection("north")
                self.spin()
                going = self.checkWall()
                while going:
                    self.move()
                    going = self.checkWall()
            elif markers[0].id in self.wallThings[1]:
                self.faceDirection("east")
                self.R.motor_board.motors[0].power = -0.5
                self.R.motor_board.motors[1].power = 0.5
                self.R.sleep(0.5)
                self.R.motor_board.motors[0].power = 0
                self.R.motor_board.motors[1].power = 0

                going = self.checkWall()
                while going:
                        
                    self.move()
                    going = self.checkWall()
            markers = self.checkWall()
            self.R.servo_board.servos[0].position = -1
            self.R.servo_board.servos[1].position = -1

            #for i in range(idx+1):
             #   self.R.motor_board.motors[0].power = 0.5
              #  self.R.motor_board.motors[1].power = 0.5
               # self.R.sleep(0.5)
                #self.R.motor_board.motors[0].power = 0
                #self.R.motor_board.motors[1].power = 0
    #        self.R#.servo_board.servos[0].position = -1
     #       self.R.servo_board.servos[1].position = -1
      #      self.R.motor_board.motors[0].power = -0.5
       #     self.R.motor_board.motors[1].power = -0.5
        #    self.R.sleep(0.5)
         #   self.R.motor_board.motors[0].power = 0
        #    self.R.motor_board.motors[1].power = 0

        #    self.spin()
#
 #           for i in range(3):
  #              self.R.motor_board.motors[0].power = 0.5
   #             self.R.motor_board.motors[1].power = 0.5
    #            self.R.sleep(0.5)
     #           self.R.motor_board.motors[0].power = 0
      #          self.R.motor_board.motors[1].power = 0
    
    
    def fetchTokens(self, corner):
        
        if corner >= 4:
            self.fetchTokens(0)
            

        foundWallMarker = False
        #self.countForCorner = 0
        turn = 0
        while turn < 10:
            self.R.motor_board.motors[0].power = 0.3
            self.R.motor_board.motors[1].power = -0.3
            self.R.sleep(0.2)
            self.R.motor_board.motors[0].power = 0
            self.R.motor_board.motors[1].power = 0

            foundWallMarker = self.facingCorner(corner)
            print(f"foundwallmarker: {foundWallMarker}")

            if foundWallMarker:
                return
                #self.faceMarker(self.markerToFace)

            turn += 1
        
        if foundWallMarker == False:
            print("oh no")
            self.fetchTokens(corner+1)


    #in case we are stuck or cant see anything: drives back and turns roughly 180 degrees
    def escape(self):
        #drive back
        self.R.motor_board.motors[0].power = -1
        self.R.motor_board.motors[1].power = -1
        self.R.sleep(0.5)
        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0

        #turn 180 degrees
        self.R.motor_board.motors[0].power = 0.5
        self.R.motor_board.motors[1].power = -0.5
        self.R.sleep(0.5)
        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0

    #method to run at start of code to find out what corner the robot is in
    #ends with robot turning roughly 90 degrees left into enermy corner (unless escape method is somehow done)
    def knowHome(self):

        count = 0
        breakFlag = False
        whileFlag = True
        
        #turns around the robot by roughly 180 degrees to see the wall markers behind it
        self.move()
        self.R.motor_board.motors[0].power = 0.5
        self.R.motor_board.motors[1].power = -0.5
        self.R.sleep(0.5)
        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0
        

        #while loop until a target marker has been found
        while whileFlag:
            markers = self.R.camera.see_ids()
            if self.seeWallMarkers(markers):
                
                #sees what corner the wall markers it is seeing is in
                for corner in self.wallMarkers:
                    for marker in corner:
                        if marker in markers:
                            self.cornerNum = count
                            breakFlag = True
                            break

                    if breakFlag:
                        break

                    count += 1
                
                self.home = self.cornerNum
                whileFlag = False
            else:
                self.spin()
                self.move()


        
        
        
    
        

    #input of target refers to which corner's marker you are trying to find: 
    # "home" = 0, 
    # "adjacent" = 1, 
    # "opposite" = 2, 
    # "end" = 3
    #output of True if robot is facing home corner and False if the robot is not
    def facingCorner(self, n):

        print(f" We on {n}")

        self.markerToFace = None
        
        #modulus wrap around to deal with the home corner being varied
        #if self.home + n >= (len(self.wallMarkers)):
        #    corner = (self.home + n) % (len(self.wallMarkers))
        #else:
        #    corner = self.home + n
        corner = (self.home + int(n)) % (len(self.wallMarkers))
        
        #list of the wall markers we would want to face towards
        wallMarkersWeWant = self.wallMarkers[corner]
        
        markers = self.R.camera.see_ids()
        if self.seeWallMarkers(markers):
            
            #checks whether the markers we are looking for are within the vision of the robot
            for marker in markers:
                if marker in wallMarkersWeWant:
                
                #attribute is updated to the marker that the robot is seeing and within the wall makrers we are targetting for
                #this attribute can be used to identify which marker the robot needs to turn to
                    self.markerToFace = marker
                    #self.countForCorner += 1
                    return True
                
        return False
    
    
    
    #Will be used to see if robot is seeing wall Markers (only the ones we care about)
    #returns True if robot is seeing wall markers
    def seeWallMarkers(self, listy):
        count = 0
        for i in range(len(listy)):
            #if listy[i] == 99 or listy[i] == 3 or listy[i] == 10 or listy[i] == 17 or listy[i] == 24:
            if listy[i] == 99:
                count += 1
        
        if count < len(listy):
            return True
        
        return False

    def dropTokens(self, corner = 0):

        if corner >= 4:
            return

        foundWallMarker = False
        #self.countForCorner = 0
        turn = 0
        while turn < 10:
            self.R.motor_board.motors[0].power = 0.3
            self.R.motor_board.motors[1].power = -0.3
            self.R.sleep(0.2)
            self.R.motor_board.motors[0].power = 0
            self.R.motor_board.motors[1].power = 0

            foundWallMarker = self.facingCorner(corner)
            print(f"foundwallmarker: {foundWallMarker}")

            if foundWallMarker:
                self.targetCorner = corner
                return

            turn += 1
        
        if foundWallMarker == False:
            print("oh no")
            self.fetchTokens(corner+1)

    def checkingMarker(self, markerToCheck):
        stop = False
        markers = self.R.camera.see()
        print(f"marker to check: {markerToCheck}")
        
        for marker in markers:
            print(marker.id)
            print(marker.distance)

            if marker.distance < 1000 and (marker.id == markerToCheck.id):
                print(marker.id)
                print(marker.distance)
                stop = True
        
        return stop


    def checkSpecificMarker(self, markersToCheck):
        stop = False
        markers = self.R.camera.see()
        
        for marker in markers:
            #print(marker.id)
            #print(marker.distance)

            if marker.distance < 1000 and (marker.id in markersToCheck):
                print(marker.id)
                print(marker.distance)
                stop = True
        
        return stop
                

    def right(self):
        self.R.motor_board.motors[0].power = 0.5
        self.R.motor_board.motors[1].power = -0.5
        self.R.sleep(0.25)
        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0


    def testMethod(self):

        self.fetchTokens(1)

        self.faceClosestToken(1)

        noCollision = True

        while noCollision:
            self.R.motor_board.motors[0].power = 1
            self.R.motor_board.motors[1].power = 1
            self.R.sleep(0.1)
            noCollision = self.checkMarker()
        
        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0

        if self.nearToken:
            self.R.servo_board.servos[0].position = 0.9
            self.R.servo_board.servos[1].position = 0.9
            self.R.sleep(0.3)
            self.escape()
        


        self.dropTokens()

        self.faceMarker(self.markerToFace)

        actualCorner = self.home + self.targetCorner % (len(self.wallMarkers))
        markerstoCheck = self.wallMarkers[actualCorner]

        atCorner = False
        count = 0

        while atCorner == False:
            self.R.motor_board.motors[0].power = 1
            self.R.motor_board.motors[1].power = 1
            self.R.sleep(0.1)
            atCorner = self.checkSpecificMarker(markerstoCheck)
            count += 1

            if count > 20:
                break
        
        print("done")
        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0

        self.R.servo_board.servos[0].position = -1
        self.R.servo_board.servos[1].position = -1
        self.R.sleep(0.3)
        self.escape()

        #self.R.motor_board.motors[0].power = 1
        #self.R.motor_board.motors[1].power = 1
        #self.R.sleep(0.5)
        #self.R.motor_board.motors[0].power = 0
        #self.R.motor_board.motors[1].power = 0
    

    #def main(self):
        #self.knowHome()
        #while True:
            #pass
    
    def ninety(self, direction = "east"):
        if direction == "east":
            self.R.motor_board.motors[0].power = 0.5
            self.R.motor_board.motors[1].power = -0.5
            self.R.sleep(0.27)
            self.R.motor_board.motors[0].power = 0
            self.R.motor_board.motors[1].power = 0
        else:
            self.R.motor_board.motors[0].power = -0.5
            self.R.motor_board.motors[1].power = 0.5
            self.R.sleep(0.27)
            self.R.motor_board.motors[0].power = 0
            self.R.motor_board.motors[1].power = 0
        
    def halfturn(self):
            self.R.motor_board.motors[0].power = 0.5
            self.R.motor_board.motors[1].power = -0.5
            self.R.sleep(0.52)
            self.R.motor_board.motors[0].power = 0
            self.R.motor_board.motors[1].power = 0

    def spinNface(self):
        closestMarker = None
        wallMarkers = self.searchForWalls()
        if len(wallMarkers) > 0:
            closestMarker = wallMarkers[0].id
            if closestMarker in self.wallThings[self.cornerNum % 4]:
                self.faceDirection("north")
            if closestMarker in self.wallThings[(self.cornerNum + 1) % 4]:
                self.faceDirection("east")
            if closestMarker in self.wallThings[(self.cornerNum + 2) % 4]:
                self.faceDirection("south")
            if closestMarker in self.wallThings[(self.cornerNum + 3) % 4]:
                self.faceDirection("west")
        
        self.R.motor_board.motors[0].power = 0.4
        self.R.motor_board.motors[1].power = 0.4
        self.R.sleep(0.4)
        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0
            
        
        return closestMarker
        

    def see(self):
        markers = self.R.camera.see()
        print(markers)

        for marker in markers:
            if marker.id < 28:
                if marker.distance < 1000:
                    return True
        return False

    def checkWeight(self):
        self.R.servo_board.servos[2].position = 1
        self.R.servo_board.servos[3].position = 1
        weight1 = self.R.ruggeduino.pins[A6].analogue_read()
        weight2 = self.R.ruggeduino.pins[A7].analogue_read()
        self.R.sleep(0.1)
        self.R.servo_board.servos[2].position = -1
        self.R.servo_board.servos[3].position = -1
        return weight1, weight2
    
    def fetch(self):
        self.faceDirection("north")

        targetMarker = self.findClosestCornerMarker(1)
        if targetMarker != None:
            print(f" closest corner marker {targetMarker.id}")
            self.newFaceMarker(targetMarker.id)
            self.R.sleep(2)
        #self.R.motor_board.motors[0].power = 0.15
        #self.R.motor_board.motors[1].power = -0.15
        #self.R.sleep(0.1)
        #self.R.motor_board.motors[0].power = 0
        #self.R.motor_board.motors[1].power = 0
        
            

        for corner in self.wallMarkers:
            if targetMarker.id in corner:
                wantedMarkers = corner

        print(f"wanted markers: {wantedMarkers}")
        
        atMarker = False
        count3 = 0

        while atMarker == False:
            self.R.motor_board.motors[0].power = 0.5
            self.R.motor_board.motors[1].power = 0.5
            self.R.sleep(0.1)


            atMarker = self.checkSpecificMarker(wantedMarkers)
            if atMarker == False:
                count3 += 1
            
            if count3 > 40:
                atMarker = True
                print("stopped")
        
        self.ninety()
        self.R.motor_board.motors[0].power = 0.5
        self.R.motor_board.motors[1].power = 0.5
        self.R.sleep(0.25)
        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0
        
        self.faceClosestToken(1)

        noCollision = True
        count2 = 0

        while noCollision:
            self.R.motor_board.motors[0].power = 0.8
            self.R.motor_board.motors[1].power = 0.8
            self.R.sleep(0.1)
            noCollision = self.checkMarker()
            if noCollision == True:
                count2 += 1
            
            if count2 > 40:
                noCollision = False
                print("was stuck when in fetch stage")
        
        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0

        if self.nearToken:
            self.R.servo_board.servos[0].position = 0.8
            self.R.servo_board.servos[1].position = 0.8
            self.R.sleep(0.3)
            #print(self.checkWeight())
        
        self.R.sleep(0.5)
    
    def retrive(self):
        marker = self.spinNface()

        self.R.sleep(1)

        print(self.direction)


        turn = None


        if marker in self.wallMarkers[(self.cornerNum) % 4]:
            self.repeat = 0
            turn = 0

        elif marker in self.wallMarkers[(self.cornerNum + 1) % 4]:
            self.repeat = 0
            if self.direction == "north":
                turn = 3
            elif self.direction == "east":
                turn = 2
            elif self.direction == "south":
                turn = 1
            elif self.direction == "west":
                turn = 0

        elif marker in self.wallMarkers[(self.cornerNum + 2) % 4]:
            self.repeat = 1
            if self.direction == "north":
                turn = 0
            elif self.direction == "east":
                turn = 3
            elif self.direction == "south":
                turn = 2
            elif self.direction == "west":
                turn = 1

        elif marker in self.wallMarkers[(self.cornerNum + 3) % 4]:
            self.repeat = 0
            if self.direction == "north":
                turn = 0
            elif self.direction == "east":
                turn = 3
            elif self.direction == "south":
                turn = 2
            elif self.direction == "west":
                turn = 1

        print(turn)

        if turn == 1:
            self.ninety()
            print("turned ninety (east)")
        elif turn == 2:
            self.halfturn()
            print("turned 180")
        if turn == 3:
            self.ninety("west")
            print("turned ninety (west)")
                

        
        self.R.sleep(0.5)

        targetMarker = self.findClosestCornerMarker(-1)
        print(f"Target marker to go home: {targetMarker}")

        if targetMarker != None:
            self.newFaceMarker(targetMarker.id)
            self.R.sleep(2)
        self.R.motor_board.motors[0].power = 0.15
        self.R.motor_board.motors[1].power = -0.15
        self.R.sleep(0.1)
        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0
        

        for corner in self.wallMarkers:
            if targetMarker.id in corner:
                wantedMarkers = corner
        
        #atMarker = False
        #count3 = 0

        #while atMarker == False:
        #    self.R.motor_board.motors[0].power = 0.5
        #    self.R.motor_board.motors[1].power = 0.5
         #   self.R.sleep(0.1)


            #atMarker = self.checkSpecificMarker(wantedMarkers)
            #if atMarker == False:
            #    count3 += 1
            
           # if count3 > 40:
             #   atMarker = True
              #  print("stopped")

        

        #markerstoCheck = self.wallMarkers[self.cornerNum % 4]
        markerstoCheck = corner
        atCorner = False
        count = 0

        while atCorner == False:
            self.R.motor_board.motors[0].power = 1
            self.R.motor_board.motors[1].power = 1
            self.R.sleep(0.1)
            atCorner = self.checkSpecificMarker(markerstoCheck)
            if atCorner == False:
                count += 1
            
            if count > 20:
                atCorner = True
                print("stopped")

        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0

        self.R.sleep(0.4)

    
    def final(self):
        self.knowHome()

        while True:
            self.repeat = 1
            self.fetch()

            while self.repeat != 0:
                self.retrive()
                self.R.sleep(0.1)
            
            self.R.servo_board.servos[0].position = -1
            self.R.servo_board.servos[1].position = -1

            self.R.motor_board.motors[0].power = -0.5
            self.R.motor_board.motors[1].power = -0.5
            self.R.sleep(0.5)
            self.R.motor_board.motors[0].power = 0
            self.R.motor_board.motors[1].power = 0
            
            
            #self.spinNface()
            #edgeMarker = self.searchForWalls()[0].id
            #while edgeMarker != (self.middleMarkers[self.cornerNum%4] or self.middleMarkers[(self.cornerNum + 1)%4]:
             #   self.R.motor_board.motors[0].power = -0.5
              #  self.R.motor_board.motors[1].power = -0.5
               # self.R.sleep(1)
                #self.R.motor_board.motors[0].power = 0
              #  self.R.motor_board.motors[1].power = 0
              #  edgeMarker = self.searchForWalls()[0].id
            print("done")

        





r = robot()
r.final()
#r.newFaceMarker(9)
