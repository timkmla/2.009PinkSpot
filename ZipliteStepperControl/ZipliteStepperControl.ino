/* 

*/

#include <Wire.h>
#include <Adafruit_MotorShield.h>

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

// Connect a stepper motor with 200 steps per revolution (1.8 degree) to motor port #2 (M3 and M4)
Adafruit_StepperMotor *myMotorPan = AFMS.getStepper(200, 1);
Adafruit_StepperMotor *myMotorTilt = AFMS.getStepper(200, 2);

int PanGearRatio = 5.5;
int TiltGearRatio = 3.95;

int CurrentTilt = 0;          // Needs to be negative or zero
int CurrentPan = 0;           // Needs to be negative or zero
int PositionTilt = 0;
int PositionPan = 0;
int TiltStepAmt = 0;
int PanStepAmt = 0;
int deltaTilt = 0;
int deltaPan = 0;

void setup()
{
  Serial.begin(9600);

  AFMS.begin(1000);
  myMotorPan->setSpeed(50);
  myMotorTilt->setSpeed(50);
}

void loop()
{
  if (Serial.available()>0)
  {
    long int InputData = Serial.parseInt();
    String PositionData = String(InputData);
    if ((PositionData.substring(0,3).toInt()) == 255)
    {
      PositionTilt = PositionData.substring(3,6).toInt();
      PositionPan = PositionData.substring(6).toInt();
      
      deltaTilt = (PositionTilt - CurrentTilt);
      deltaPan = (PositionPan - CurrentPan);
      
      TiltStepAmt = abs(round((deltaTilt/1.8)*TiltGearRatio));
      PanStepAmt = abs(round((deltaPan/1.8)*PanGearRatio));
      
      //if (deltaTilt < 0)
      //{
      //  myMotorTilt->step(TiltStepAmt, FORWARD, DOUBLE);
      //}
      //if (deltaTilt > 0)
      //{
      //  myMotorTilt->step(TiltStepAmt, BACKWARD, DOUBLE);
      //}
      
      if (deltaPan < 0)
      {
        myMotorPan->step(PanStepAmt, FORWARD, DOUBLE); 
      }
      if (deltaPan > 0)
      {
        myMotorPan->step(PanStepAmt, BACKWARD, DOUBLE);
      }
      
      CurrentTilt = PositionTilt;
      CurrentPan = PositionPan;
    }
  }
}
