/***********************************************************************************************************
/* Lidar Lite Sweep scan
/* By: Ben Nakash
/* Date: 23-01-2016
/* 
/* Short example based on the Servo library example "Sweep" example and the Pulsed Light 3D examples.
/* The servo motor is attached to pin 9 and rotates from 0-40 degrees continuously by 1 degree increments.
/* The LIDAR lite is attached to VCC (+5 V DC), GND, SDA and SCL.
/* This examples uses the Wire library.
/**********************************************************************************************************/

#include <Wire.h>

#define    LIDARLite_ADDRESS   0x62          // Default I2C Address of LIDAR-Lite.
#define    RegisterMeasure     0x00          // Register to write to initiate ranging.
#define    MeasureValue        0x04          // Value to initiate ranging.
#define    RegisterHighLowB    0x8f          // Register to get both High and Low bytes in 1 call.

#include <Servo.h>

Servo myservo;

int pos = 0;         // Position of the servo (degress, [0, 180])
int distance = 0;    // Distance measured
int servoPin = 9;

void setup()
{
  // Serial output
  Serial.begin(9600);
  Serial.println("< START >");
  
  // Servo control
  myservo.attach(servoPin, 771, 1798);
  
  // LIDAR control
  Wire.begin(); // join i2c bus
}

// Get a measurement from the LIDAR Lite
int lidarGetRange(void)
{
  int val = -1;
  
  Wire.beginTransmission((int)LIDARLite_ADDRESS); // transmit to LIDAR-Lite
  Wire.write((int)RegisterMeasure); // sets register pointer to  (0x00)  
  Wire.write((int)MeasureValue); // sets register pointer to  (0x00)  
  Wire.endTransmission(); // stop transmitting

  delay(20); // Wait 20ms for transmit

  Wire.beginTransmission((int)LIDARLite_ADDRESS); // transmit to LIDAR-Lite
  Wire.write((int)RegisterHighLowB); // sets register pointer to (0x8f)
  Wire.endTransmission(); // stop transmitting

  delay(20); // Wait 20ms for transmit
  
  Wire.requestFrom((int)LIDARLite_ADDRESS, 2); // request 2 bytes from LIDAR-Lite

  if(2 <= Wire.available()) // if two bytes were received
  {
    val = Wire.read(); // receive high byte (overwrites previous reading)
    val = val << 8; // shift high byte to be high 8 bits
    val |= Wire.read(); // receive low byte as lower 8 bits
  }
  
  return val;
}

void serialPrintRange(int pos, int distance)
{
    Serial.print("Position (deg): ");
    Serial.print(pos);
    Serial.print("\t\tDistance (cm): ");
    Serial.println(distance);
}

void loop()
{
  distance = lidarGetRange();
  serialPrintRange(pos, distance);
  for(pos = 0; pos <= 40; pos += 1)
  {
    myservo.write(pos);
    distance = lidarGetRange();
    serialPrintRange(pos, distance);
    delay(15);
  }
  for(pos = 40; pos>0; pos-=1)
  {
    myservo.write(pos);
    distance = lidarGetRange();
    serialPrintRange(pos, distance);
    delay(15);
  }
}

