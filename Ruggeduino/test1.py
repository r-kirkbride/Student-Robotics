from sr.robot3 import Robot as R

print(f"Left Motor: {R.ruggeduino.command("x")} degrees")
print(f"Right Motor: {R.ruggeduino.command("y")} degrees")