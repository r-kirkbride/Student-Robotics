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


    def drive(self, times = 0.5):
        self.R.motor_board.motors[0].power = 0.5
        self.R.motor_board.motors[1].power = 0.5
        time.sleep(times)
        self.R.motor_board.motors[0].power = 0
        self.R.motor_board.motors[1].power = 0

    
    def grabToken(self):
        self.moveDist(600)
        self.R.ruggeduino.command("c")
        time.sleep(0.5)
        self.R.ruggeduino.command("b")
    
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
        
        print("donee")
    
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
