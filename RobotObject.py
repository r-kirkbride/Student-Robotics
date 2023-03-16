from sr.robot3 import *
import time
import math

class robot:
    
    def __init__(self):
        
        #Creates an instance of the robot object from sr.robot3 and saves it as in attribute to the instance of this class
        self.R = Robot() 
        
        markers = self.R.camera.see_ids()
        
        self.R.ruggeduino.command("s") #reset motor encoders
        
        self.zone = self.R.zone

        if self.zone == 3:
            self.homeMarkers = [18,19,20,21,22,23]
        elif self.zone == 2:
            self.homeMarkers = [11,12,13,14,15,16]
        elif self.zone == 1:
            self.homeMarkers = [4,5,6,7,8,9]
        else:
            self.homeMarkers = [25,26,27,0,1,2]

        self.R.ruggeduino.command("g")

        self.R.ruggeduino.command("d")
        time.sleep(0.5)
        self.R.ruggeduino.command("e")


    # Distance in millimetres, -1 <= speed <= 1
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
        self.R.motor_board.motors[0].power = 0.5
        self.R.motor_board.motors[1].power = 0.5
        time.sleep(times)
        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0

    
    def grabToken(self):
        self.moveDist(1050)
        self.R.ruggeduino.command("c")
        time.sleep(0.5)
        self.R.ruggeduino.command("b")

    def releaseToken(self):
        self.R.ruggeduino.command("d")
        time.sleep(0.5)
        self.R.ruggeduino.command("e")
        self.moveDist(-1050)
        
    def faceMarker(self, marker_id):
        flag = False
        
        distance = 9999999999
        counting = 0

        #add clause for when counting is greater than 18 that identifies a new closeset token if we cant see any
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
                    
                    flag = True
                    break
            
            if flag == True:
                break

            counting += 1
        


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
                        
                        if tempDistance > distance or abs(tempDistance - distance) < 2.5:
                            print("facing")
                            
                            flag = True
                            break
                        else:
                            distance = tempDistance
            
            if flag == True:
                break
            
            count += 1
        
        time.sleep(0.1)

        if count >= 30:
            print("Robot stuck when looking for marker")
            
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
            
            
            angle = usedMarker.spherical.rot_y
            dist = usedMarker.distance
            while dist > 1200:
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


    def main(self):
        self.goToMarker(33)
        self.grabToken()
