from sr.robot3 import *
import time
R = Robot()

def sleep(duration):
	# if using a kit, use this:
	time.sleep(duration)
	# if using the simulator, use this
	# R.sleep(duration)

def spin(duration, speed):
    # make robot spin
    R.motor_board.motors[0].power = speed
    R.motor_board.motors[1].power = -speed
    sleep(duration)
    R.motor_board.motors[0].power = 0
    R.motor_board.motors[1].power = 0

def look_for_any_marker():
    marker_ids = R.camera.see_ids()
    if len(marker_ids) > 0:
        print ("Found a marker!")
        return marker_ids[0]

marker = None
while marker is None:
    print("Spinning to find a marker")
    duration = 0.1
    speed = 0.5
    spin(speed, duration)
    marker = look_for_any_marker()
