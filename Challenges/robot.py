from RobotObject import robot 

R = robot()

for i in range(3):
    R.faceMarker(28)
    R.moveDist(1550)
    R.faceMarker(33)
    R.moveDist(1550)
    R.faceMarker(29)
    R.moveDist(2140)
