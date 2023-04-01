from sr.robot3 import *
import time
import math

class robot:
    
    def __init__(self):
        
        #Creates an instance of the robot object from sr.robot3 and saves it as in attribute to the instance of this class

        self.R = Robot() 
        
        self.R.ruggeduino.command("s") #reset motor encoders

        #height from bottom of robot to camera tower
        self.HEIGHT = 1000 #actually about 450
        
        self.zone = self.R.zone
        self.markersList = [[25,26,27,0,1,2], [4,5,6,7,8,9], [11,12,13,14,15,16], [18,19,20,21,22,23]]
        self.homeMarkers = self.markersList[self.zone][1:-1]
        self.adjacentMarkers = self.markersList[(self.zone + 1)%4]
        self.oppositeMarkers = self.markersList[(self.zone + 2)%4]
        self.endMarkers = self.markersList[(self.zone + 3)%4]

        print(self.homeMarkers)

        self.R.ruggeduino.command("j")
        time.sleep(3)
        self.R.ruggeduino.command("b")
        time.sleep(0.3)
        self.R.ruggeduino.command("c")
        time.sleep(0.3)
    
    def moveDist(self, dist, speed=0.5,braking = True):
        CIRCUMFERENCE = 100 * math.pi #circumference of the wheels
        TOLERANCE = 5 #tolerance of difference before it compensates
        DEGREES_PER_ROT = 80
        degrees = (dist/CIRCUMFERENCE)*DEGREES_PER_ROT #number of degrees to rotate
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
            while int(self.R.ruggeduino.command("x")) > TOLERANCE and int(self.R.ruggeduino.command("y")) > TOLERANCE:
                self.R.ruggeduino.command("s")
                time.sleep(0.005)
        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0
    
    def turnDeg(self,angle,speed=0.5,braking = True): #angle in degrees
        angle = (angle/180)*math.pi
        DEGREES_PER_ROT = 90
        WHEELBASE = 400
        CIRCUMFERENCE = 100 * math.pi #circumference of the wheels
        TOLERANCE = 5 #tolerance of difference before it compensates
        dist = abs(angle) * WHEELBASE
        degrees = (dist/CIRCUMFERENCE)*DEGREES_PER_ROT #number of degrees to rotate
        reverseMultiplier = speed/abs(speed)
        self.R.ruggeduino.command("s")
        ruggeduinoCommand , motorNo = "y" , 1
        if angle >= 0:
            ruggeduinoCommand , motorNo = "x" , 0

        enc = int(self.R.ruggeduino.command(ruggeduinoCommand))
        while enc < degrees:
            print(enc)
            enc = int(self.R.ruggeduino.command(ruggeduinoCommand))
            self.R.motor_board.motors[motorNo].power = speed
            time.sleep(0.005)
        
        if braking:
            self.R.motor_board.motors[motorNo].power = -1*reverseMultiplier
            while int(self.R.ruggeduino.command(ruggeduinoCommand)) > TOLERANCE:
                self.R.ruggeduino.command("s")
                time.sleep(0.005)
        self.R.motor_board.motors[motorNo].power = 0
    
    def rotateDeg(self,angle,speed=0.5,braking = True): #angle in degrees
        angle = (angle/180)*math.pi
        speed = abs(speed)
        DEGREES_PER_ROT = 81.5
        WHEELBASE = 400
        CIRCUMFERENCE = 100 * math.pi #circumference of the wheels
        TOLERANCE = 5 #tolerance of difference before it compensates
        dist = abs(angle) * WHEELBASE * 0.5
        degrees = (dist/CIRCUMFERENCE)*DEGREES_PER_ROT #number of degrees to rotate
        self.R.ruggeduino.command("s")

        leftMultiplier , rightMultiplier = 1 , -1
        if angle < 0:
            leftMultiplier , rightMultiplier = -1 , 1
        
        encLeft = int(self.R.ruggeduino.command("x"))
        encRight = int(self.R.ruggeduino.command("y"))
        while (encLeft + encRight)/2 < degrees:
            #print(f"L:{encLeft}, {self.R.motor_board.motors[0].power}\tR:{encRight}, {self.R.motor_board.motors[1].power}")
            encLeft = int(self.R.ruggeduino.command("x"))
            encRight = int(self.R.ruggeduino.command("y"))
            if encLeft > encRight + TOLERANCE:
                self.R.motor_board.motors[0].power -= leftMultiplier * 0.005
            elif encRight > encLeft + TOLERANCE:
                self.R.motor_board.motors[1].power -= rightMultiplier * 0.005
            else:
                self.R.motor_board.motors[0].power = speed * leftMultiplier
                self.R.motor_board.motors[1].power = speed * rightMultiplier
            time.sleep(0.05)
        if braking:
            self.R.motor_board.motors[0].power = -1*leftMultiplier
            self.R.motor_board.motors[1].power = -1*rightMultiplier
            while int(self.R.ruggeduino.command("x")) > TOLERANCE and int(self.R.ruggeduino.command("y")) > TOLERANCE:
                self.R.ruggeduino.command("s")
                time.sleep(0.005)
        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0


    def drive(self, times = 0.5):
        self.R.motor_board.motors[0].power = 0.6
        self.R.motor_board.motors[1].power = 0.6
        time.sleep(times)
        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0

    
    def grabToken(self):
        #lastDist value gotten from goToMarker method
        #dist = self.lastDist
        
        #actualDist = math.sqrt((dist ** 2) - (self.HEIGHT ** 2))
        self.R.ruggeduino.command("d")
        time.sleep(0.3)
        self.R.ruggeduino.command("e")
        time.sleep(0.3)
        #value tbd during testing 
        print(f"When grabbing, lastDist = {self.lastDist}")
        self.moveDist(self.lastDist-100)
        self.R.ruggeduino.command("b")
        time.sleep(0.3)
        self.R.ruggeduino.command("c")
        time.sleep(0.3)
        self.moveDist(-800)

    def releaseToken(self):

        #lastDist value gotten from goToMarker method
        #dist = self.lastDist

        #actualDist = math.sqrt((dist ** 2) - (self.HEIGHT ** 2))
        
        #value tbd during testing 
        print(f"When releasing, lastDist = {self.lastDist}")
        self.moveDist(self.lastDist-700)

        self.R.ruggeduino.command("d")
        time.sleep(0.3)
        self.R.ruggeduino.command("e")
        time.sleep(0.3)
        self.moveDist(-800)
        self.R.ruggeduino.command("b")
        time.sleep(0.3)
        self.R.ruggeduino.command("c")
        time.sleep(0.3)
        
    def faceMarker(self, targetMarkers):
        flag = False
        
        distance = 9999999999
        counting = 0
        marker_id = None
        self.closestMarkerDistance = None
        self.closeMarker = None

        #add clause for when counting is greater than 18 that identifies a new closeset token if we cant see any
        while counting < 18:
            self.R.motor_board.motors[0].power = 0.3
            self.R.motor_board.motors[1].power = -0.3
            time.sleep(0.5)
            self.R.motor_board.motors[0].power = 0
            self.R.motor_board.motors[1].power = 0
            time.sleep(0.3)
            markers = self.R.camera.see()
            for i in range(len(markers)):
                if markers[i].id in targetMarkers:
                #if markers[i].id == marker_id:
                    distance = markers[i].distance
                    self.closestMarkerDistance = distance
                    marker_id = markers[i].id
                    print("honed in")
                    
                    flag = True
                    break
            
            if flag == True:
                break

            counting += 1
            
        return marker_id

    



    def goToMarker(self, marker_id, speed=0.5, minDist=1100):

        self.lastDist = 800

        #self.faceMarker(marker_id)
        markers = self.R.camera.see()
        usedMarker = None
        for marker in markers:
            if marker.id == marker_id:
                usedMarker = marker
        if usedMarker == None:
            return
        else:
            print(f"used marker id: {usedMarker.id}")
            #adds 50mm buffer between robot and object
            counter = 0
            
            
            angle = usedMarker.spherical.rot_y
            dist = usedMarker.distance
            while dist > minDist:
                print(f"{usedMarker.distance}")
                angle = usedMarker.spherical.rot_y
                dist = usedMarker.distance
                self.drive(times = 0.5)
                markers = self.R.camera.see()
                marker_ids = []
                for m in markers:
                    marker_ids.append(m.id)
                    if m.id == usedMarker.id:
                        angle = m.spherical.rot_y
                        dist = m.distance
                        self.lastDist = dist
                        break
                print(f"distance: {dist}")
                print(f"marker ids: {marker_ids}")
                if angle > 0:
                    speed = -0.15
                else:
                    speed = 0.15
                print(angle)
                print(speed)
                if abs(angle) > 0.08:
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
        
        print("donee")

    def goHome(self):
        markers = self.R.camera.see()
        for marker in markers:
            if marker.id in self.homeMarkers:
                self.goToMarker(marker.id)
                return

    def goAdjacent(self):
        markers = self.R.camera.see_ids()
        for marker in markers:
            if marker in self.adjacentMarkers:
                self.goToMarker(marker, minDist=2875)
                return
    
    def searchForTokens(self):
        fullMarkers = []
        for i in range(9):
            self.R.motor_board.motors[0].power = -0.5
            self.R.motor_board.motors[1].power = 0.5
            time.sleep(0.3)
            self.R.motor_board.motors[0].power = 0
            self.R.motor_board.motors[1].power = 0
            time.sleep(0.3)
            markers = self.R.camera.see()
            markers = [marker for marker in markers if marker.id > 27]
            for marker in markers:
                if marker in fullMarkers:
                    markers.remove(marker)
            fullMarkers += markers
        markers = sorted(fullMarkers, key=lambda x: x.distance)

    def goClosestHome(self):
        markers = self.R.camera.see()
        usedId = 809
        for marker in markers:
            if marker in self.homeMarkers:
                usedId = marker
                break
        self.goToMarker(usedId)
    
    def fetch(self, targetMarkers):


        markers = self.R.camera.see_ids()

        if self.count == 0:

            self.goToMarker(73)
            print("we have gone to 73, to be grabbed")
            #dist = 2
            self.grabToken()
            print("box grabbed")
            self.rotateDeg(-180)
            return
            
        else:

            wantedMarkers = []

            for marker in markers:
                if marker in targetMarkers:
                    wantedMarkers.append(marker)
            
            if len(wantedMarkers) != 0:
                
                #CHANGE TO 1000 FOR THE ACTUAL COMPETITION (MAYBE)
                self.moveDist(500)
                #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
                if 73 in markers:

                    self.goToMarker(73)
                    self.grabToken()
                    self.rotateDeg(-180)

                else:
                    
                    if self.fetchTargetMarkers == self.markersList[(self.zone + 1)% 4][0:-1]:
                        
                        self.fetchTargetMarkers = self.markersList[(self.zone + 3)% 4][0:-1]
                    else:
                        self.fetchTargetMarkers = self.markersList[(self.zone + 1)% 4][0:-1]
                    
                    self.repeat = True
                    return

                    
                    #self.rotateDeg(60)

                    #markers = self.R.camera.see_ids()
                    
                    #if 73 in markers:
                        #self.goToMarker(73)
                        #self.grabToken()
                        #self.rotateDeg(-180)
                    
                    #else:

                        #self.rotateDeg(-120)

                        #markers = self.R.camera.see_ids()
                        
                        #if 73 in markers:
                           # self.goToMarker(73)
                            #self.grabToken()
                           # self.rotateDeg(-180)
                        
                        #else:
                           # self.fetchTargetMarkers = self.markersList[(self.zone + 3)% 4][0:-1]
                           # return

            
            else:

                closestMarker = self.faceMarker(targetMarkers)

                if closestMarker != None:
        
                    markers = self.R.camera.see_ids()

                    if 73 in markers:
                        #CHANGE TO 1000 FOR THE ACTUAL COMPETITION (MAYBE)

                        #actualclosestMarkerDistance = math.sqrt((self.closestMarkerDistance ** 2) - (self.HEIGHT ** 2))

                        if self.closestMarkerDistance > 700:
                            self.moveDist(500)  #maybe this is causing the robot to run into the wall
                        self.goToMarker(73)
                        self.grabToken()
                        self.rotateDeg(-180)
                    
                    else:

                        self.goToMarker(closestMarker, 1600)
                        
                        #should turn 90 clockwise
                        self.rotateDeg(90)
                        markers = self.R.camera.see_ids()
                        if 73 in markers:
                        
                            self.goToMarker(73)
                            self.grabToken()
                            self.rotateDeg(120)
                        
                        else:
                            
                            if self.fetchTargetMarkers == self.markersList[(self.zone + 1)% 4][0:-1]:
                        
                                self.fetchTargetMarkers = self.markersList[(self.zone + 3)% 4][0:-1]
                            else:
                                self.fetchTargetMarkers = self.markersList[(self.zone + 1)% 4][0:-1]
                            
                            self.repeat = True
                            return 
                            
                            #self.rotateDeg(30)

                            #markers = self.R.camera.see_ids()
                            
                            #wantedMarkers = []

                            #for marker in markers:
                            #    if marker in targetMarkers:
                            #        wantedMarkers.append(marker)
                            #if 73 in markers and len(wantedMarkers) != 0:
                            #    self.goToMarker(73)
                            #    self.grabToken()
                            #    self.rotateDeg(-180)
                            
                            #else:

                            #    self.rotateDeg(-60)

                            #    markers = self.R.camera.see_ids()
                             #   wantedMarkers = []

                             #   for marker in markers:
                             #       if marker in targetMarkers:
                             #           wantedMarkers.append(marker)
                              #  if 73 in markers and len(wantedMarkers) != 0:
                              #      self.goToMarker(73)
                               #     self.grabToken()
                                #    self.rotateDeg(-180)
                                
                                #else:
                                #    return

                else:
                    #place to put escape method because no disered markers can be seen
                    pass

        

        ###optional (assume not part of the rest of the code)
        ##to search for the closest marker out of targetMarkers it can see rather than just the first one it can see
        ##if we are to use it, we need to change the method to return the closest marker out of the list of targetMarkers we pass into it
        ##also we need to change what we pass to goToMarker just below + the if statement to see if we should grab tokens
        #target = self.searchForTokens(targetMarkers)


        ##takes in the list of wall markers. Faces and goes to first adjacent enemy marker it sees
        ##have it so that it stops a larger distance before the target wall marker than it would for a token
        #self.gotoMarker(targetMarkers)

        ##only goes for tokens once we have gone to the markers we really wanted rather than some intermediate markers
        #if targetMarkers == self.wallMarkers[(self.zone + 1) % 4]

            ##still takes in a list. Faces and goes to closest token
            #self.gotoMarker([73])

            ##grabs token
            #self.grabToken()

            ##does a 180 turn
            #self.rotateDeg(180)
        

    def retrive(self, targetMarkers):


        turn = 180
       #if (self.count % 3) == 0:
        #    turn = 180
        #elif (self.count % 3) == 1:
        #    turn = 60
        #elif (self.count % 3) == 2:
         #   turn = -60

        markers = self.R.camera.see_ids()

        wantedMarkers = []

        for marker in markers:
            if marker in targetMarkers:
                wantedMarkers.append(marker)
            
        if len(wantedMarkers) != 0:

            self.goToMarker(wantedMarkers[0], minDist=1050)
            self.releaseToken()
            self.rotateDeg(turn)
        
        else:

            closestMarker = self.faceMarker(targetMarkers)

            if closestMarker != None:

                self.goToMarker(closestMarker, minDist=1050)
                self.releaseToken()
                self.rotateDeg(turn)
            
            else:
                

                #IMPORTANT
                #currently only working in adjacent corner
                if self.fetchTargetMarkers == self.markersList[(self.zone + 1)% 4][0:-1]:
                        
                    closeToReturningCorner = self.adjacentMarkers[0:2]
                else:
                    closeToReturningCorner = self.endMarkers[4:6]
                

                closestMarker = self.faceMarker(closeToReturningCorner)

                #im assuming we can see it
                if closestMarker != None:
                    
                    self.goToMarker(closestMarker, minDist=1000)

                    #should turn 90 anticlockwise
                    self.rotateDeg(-90)

                    self.repeat = True


                else:
                    print("HOW HAS THIS HAPPENED???????")
                    
            

            
            


        
        ###optional (assume not part of the rest of the code)
        ##to search for the closest target out of targetMarkers it can see rather than just the first one it can see
        ##if we are to use it, we need to change the method to return the closest marker out of the list of targetMarkers we pass into it
        ##also we need to change what we pass to goToMarker just below + the if statement to see if we should release tokens
        #target = self.searchForTokens(targetMarkers)

        ##takes in list of wall markers. Faces and goes to first home marker it sees
        ##have it so that it stops a larger distance before the target wall marker than it would for a token
        #self.gotoMarker(targetMarkers)

        

        ##only release tokens once we have gone to the markers we really wanted rather than some intermediate markers
        #if targetMarkers == self.homeMarkers

            ##releases token
            #self.releaseToken()

            ##does a 180 turn
            #self.rotateDeg(180)
        pass

    
    def main(self):

        start = time.time()

        self.count = 0

        #self.goToMarker(73)
        #self.grabToken()
        #self.rotateDeg(180)
        self.fetchTargetMarkers = self.markersList[(self.zone + 1) % 4][0:-1]
        print(self.fetchTargetMarkers)
        
        while True:
            
            ##which markers we will be driving to in the fetch stage
            ##reason for this is that this variable can change if robot cant see desired markers
            ##therefore making it easy to redo the same fetch sequence but with different wall markers
            
            self.repeat = True

            #repeats until repeat is not needed
            while self.repeat == True:
                
                if time.time() - start > 120:
                    self.fetchTargetMarkers = self.markersList[(self.zone + 1)% 4][0:-1]
                #if (self.count % 3) == 2:

                 #   if time.time() - start < 120:
                  #      self.fetchTargetMarkers = self.markersList[(self.zone + 3) % 4]
                   # else:
                    #    self.fetchTargetMarkers = self.markersList[(self.zone + 1) % 4]
                #else:
                 #   self.fetchTargetMarkers = self.markersList[(self.zone + 1) % 4]

                self.repeat = False
                print("running fetch")
                self.fetch(self.fetchTargetMarkers)
                
            


            ##which markers we will be driving to in the retrieve stage
            ##reason for this is that this variable can change if robot cant see desired markers
            ##therefore making it easy to redo the same retrieve sequence but with different wall markers
            self.retrieveTargetMarkers = self.homeMarkers
            self.repeat = True

            #repeats until repeat is not needed
            while self.repeat == True:
                self.repeat = False
                print("running retrieve")
                self.retrive(self.retrieveTargetMarkers)
            
            self.count += 1
