#include <Arduino.h>

// We communicate with the power board at 115200 baud.
#define SERIAL_BAUD 115200

#define FW_VER 1

//KEGS SR additions begin
int motors[2] = {0,0};
int currentL;
int currentR;
int previousL;
int previousR;
//KEGS SR additions end

void setup() {
  Serial.begin(SERIAL_BAUD);
  //KEGS SR additions begin
  pinMode(4, INPUT_PULLUP);
  pinMode(2, INPUT_PULLUP);
  pinMode(3, INPUT_PULLUP);
  pinMode(5, INPUT_PULLUP);
  previousL = digitalRead(2);
  previousR = digitalRead(3);
  //KEGS SR additions end
}

int read_pin() {
  while (!Serial.available());
  int pin = Serial.read();
  return (int)(pin - 'a');
}

void command_read() {
  int pin = read_pin();
  // Read from the expected pin.
  int level = digitalRead(pin);
  // Send back the result indicator.
  if (level == HIGH) {
    Serial.write('h');
  } else {
    Serial.write('l');
  }
}

void command_analogue_read() {
  int pin = read_pin();
  int value = analogRead(pin);
  Serial.print(value);
}

void command_write(int level) {
  int pin = read_pin();
  digitalWrite(pin, level);
}

void command_mode(int mode) {
  int pin = read_pin();
  pinMode(pin, mode);
}

//KEGS SR additions begin
void command_rotation_read(int motor) {
  Serial.print(motors[motor]);
}

void command_rotation_reset() {
  motors[0] = 0;
  motors[1] = 0;
}

//KEGS SR additions end

void loop() {
  // Fetch all commands that are in the buffer
  while (Serial.available()) {
    currentL = digitalRead(2);
    currentR = digitalRead(3);
    if ((currentL == 1) && (previousL == 0)){
      motors[0] ++;
    }
    if ((currentR == 1) && (previousR == 0)){
      motors[1] ++;
    }
    previousL = currentL;
    previousR = currentR;
    int selected_command = Serial.read();
    // Do something different based on what we got:
    switch (selected_command) {
      case 'a':
        command_analogue_read();
        break;
      case 'r':
        command_read();
        break;
      case 'l':
        command_write(LOW);
        break;
      case 'h':
        command_write(HIGH);
        break;
      case 'i':
        command_mode(INPUT);
        break;
      case 'o':
        command_mode(OUTPUT);
        break;
      case 'p':
        command_mode(INPUT_PULLUP);
        break;
      case 'v':
        Serial.print("SRcustom:");
        Serial.print(FW_VER);
        break;
      // KEGS SR additions begin
      case 'x':
        command_rotation_read(0);
        break;
      case 'y':
        command_rotation_read(1);
        break;
      case 's':
        command_rotation_reset();
        break;
      //KEGS SR additions end
      default:
        // A problem here: we do not know how to handle the command!
        // Just ignore this for now.
        break;
    }
    Serial.print("\n");
  }
}
