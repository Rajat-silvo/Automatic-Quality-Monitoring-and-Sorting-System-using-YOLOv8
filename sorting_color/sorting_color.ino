#include <Servo.h>

Servo servo01;
Servo servo02;

#define cb 8

String dataIn;

void setup() 
{
    servo01.attach(5);
    servo02.attach(6);
    pinMode(cb, OUTPUT);
    pinMode(A0, INPUT);
    pinMode(A1, INPUT);

    Serial.begin(9600);
    servo01.write(90);
    servo02.write(90);
    delay(1000);
}

void loop() 
{
  delay(1000);

  if(digitalRead(A0)==0){
    delay(100);
    digitalWrite(cb, LOW);
    Serial.print("x");
     
    // Check for incoming data
    if (Serial.available() > 0) {
      char  dataIn = Serial.read();  // Read the data as string
      Serial.print(dataIn);

    if (dataIn == 'r') {
                digitalWrite(cb, HIGH);
                delay(5500);
                digitalWrite(cb, LOW);
                delay(500);
                servo02.write(0);
                delay(1000);
                servo02.write(90);
                delay(100);
                Serial.print("Red Tomato Sorted");
                dataIn=='v';
            }

    if (dataIn == 's'){
                digitalWrite(cb, HIGH);
                delay(8400);
                digitalWrite(cb, LOW);
                delay(500);
                servo01.write(0);
                delay(1000);
                servo01.write(90);
                delay(100);
                Serial.print("Small Tomato Sorted");
                dataIn=='u';
          }
  
    if (dataIn == 'g') {
                digitalWrite(cb, HIGH);
                Serial.print("Green Tomato will go straight");
                dataIn=='z';
            } 
      }
  }
      else
      {
      digitalWrite(cb, HIGH); //belt rotet on
      }
  }
