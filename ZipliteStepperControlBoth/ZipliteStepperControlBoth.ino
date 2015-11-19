/* 

*/

#include <AccelStepper.h>
#include <Wire.h>
#include <Adafruit_MotorShield.h>

int Pan = 0;
int Tilt = 1;

int PanGearRatio = 5.5;
int TiltGearRatio = 3.8;

long int InputData = 0;
String PositionData = "";

int PositionTilt = 0;
int PositionPan = 0;

int TiltStepAmt = 0;
int PanStepAmt = 0;

int CurrentTilt = 0;
int CurrentPan = 0;

float speed = 400.0;
float acceleration = 200.0;

Adafruit_MotorShield AFMS0 = Adafruit_MotorShield();

Adafruit_StepperMotor *PanMotor = AFMS0.getStepper(200, 1);
Adafruit_StepperMotor *TiltMotor = AFMS0.getStepper(200, 2);

void ForwardStepPan() { PanMotor->onestep(BACKWARD, DOUBLE); }
void BackwardStepPan() { PanMotor->onestep(FORWARD, DOUBLE); }
void ForwardStepTilt() { TiltMotor->onestep(BACKWARD, DOUBLE); }
void BackwardStepTilt() { TiltMotor->onestep(FORWARD, DOUBLE); }

AccelStepper steppers[2] = {AccelStepper(ForwardStepPan, BackwardStepPan), AccelStepper(ForwardStepTilt, BackwardStepTilt)};

void setup()
{
  Serial.begin(9600);

  AFMS0.begin();

  steppers[Pan].setMaxSpeed(speed);
  steppers[Pan].setAcceleration(acceleration);
  
  steppers[Tilt].setMaxSpeed(speed);
  steppers[Tilt].setAcceleration(acceleration);
}

void loop()
{
  steppers[Pan].run();    
  steppers[Tilt].run();
    
  if (Serial.available() > 0)
  {
    InputData = Serial.parseInt();
    PositionData = String(InputData);
    if ((PositionData.substring(0,3).toInt()) == 255)
    {
      PositionTilt = PositionData.substring(3,6).toInt();
      PositionPan = PositionData.substring(6).toInt();
      
      TiltStepAmt = abs(round((PositionTilt/1.8)*TiltGearRatio));
      PanStepAmt = abs(round((PositionPan/1.8)*PanGearRatio));

      if (abs((PositionPan - CurrentPan)) > 2.5)
      {
        steppers[Pan].moveTo(PanStepAmt);
        steppers[Pan].run();
      }

      if (abs((PositionTilt - CurrentTilt)) > 2.5)
      {
        steppers[Tilt].moveTo(TiltStepAmt);
        steppers[Tilt].run();
      }
    }

    CurrentPan = PositionPan;
    CurrentTilt = PositionTilt;
  }
}
