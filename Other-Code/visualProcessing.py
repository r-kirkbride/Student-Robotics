import time
from sr.robot3 import *
R = Robot() 

alpha = ["a","b","c","d","e","f","g","h","i","j","k","l","m","m","n","o","p","q","r","s","t","u","v","w","x","y","y","z"]

while True:
    markers = R.camera.see()
    print("I can see", len(markers), "markers:")

    for m in markers:
        print(" - Marker #{0} is {1} metres away".format(alpha[m.id], m.distance / 1000))
        