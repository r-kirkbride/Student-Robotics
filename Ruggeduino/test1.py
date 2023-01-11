from sr.robot3 import Robot as R

left = R.ruggeduino.command("x")
right = R.ruggeduino.command("y")
print(f"Left Motor: {left} degrees")
print(f"Right Motor: {right} degrees")