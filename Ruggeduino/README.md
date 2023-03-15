# How to use the Ruggeduino:

## How to connect motors to Ruggeduino:
- Red wires for each motor should be connected to the 5V rail.
- Black wires should be connected to the 0V rail.
- The left motor's yellow wire should be connected to digital pin 2.
- The right motor's blue wire (yellow wire with blue heatshrink on the end) should be connected to digital pin 3.

## How to interface with in python:
- `R.ruggeduino.command("x")` will return rotation in degrees since last reset of the Left motor.
- `R.ruggeduino.command("y")` will return rotation in degrees since last reset of the right motor.
- `R.ruggeduino.command("s")` will reset the rotation to 0 for both motors.

## How to connect servos to Ruggeduino:
- Red wires for each servo should be connected to the 5V rail.
- Black wires should be connected to the 0V rail.
- The yellow control signal wire for the left servo should be connected to Digital Pin 8.
- The yellow control signal wire for the right servo should be connected to Digital Pin 10.

## How to interface with in python:
- `R.ruggeduino.command("g")` sets up the servos and resets them - **MUST BE RUN BEFORE RUNNING ANY OTHER COMMAND** 
- `R.ruggeduino.command("b")` closes the left servo
- `R.ruggeduino.command("c")` closes the right servo
- `R.ruggeduino.command("d")` opens the left servo
- `R.ruggeduino.command("e")` opens the right servo
