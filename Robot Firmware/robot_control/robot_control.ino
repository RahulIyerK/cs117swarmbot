/******************
   Pin Definitions
 ******************/

//Right Motor
#define MOTOR_L_DIR_PIN 14 //P1.7
#define MOTOR_L_PWM_PIN 40 //P2.7
#define MOTOR_L_SLP_PIN 31 //P3.7

//Left Motor
#define MOTOR_R_DIR_PIN 15 //P1.6
#define MOTOR_R_PWM_PIN 39 //P2.6
#define MOTOR_R_SLP_PIN 11 //P3.6

#define FORWARD LOW
#define REVERSE HIGH

void setup() {
  // put your setup code here, to run once:
  pinMode(MOTOR_L_DIR_PIN, OUTPUT);
  pinMode(MOTOR_L_PWM_PIN, OUTPUT);
  pinMode(MOTOR_L_SLP_PIN, OUTPUT);

  pinMode(MOTOR_R_DIR_PIN, OUTPUT);
  pinMode(MOTOR_R_PWM_PIN, OUTPUT);
  pinMode(MOTOR_R_SLP_PIN, OUTPUT);

  digitalWrite(MOTOR_L_SLP_PIN, HIGH);
  digitalWrite(MOTOR_R_SLP_PIN, HIGH);

  digitalWrite(MOTOR_L_DIR_PIN, FORWARD);
  digitalWrite(MOTOR_R_DIR_PIN, FORWARD);
}

//drive forward for a set number of milliseconds
void forward(int speed, int del){
  digitalWrite(MOTOR_L_DIR_PIN, FORWARD);
  digitalWrite(MOTOR_R_DIR_PIN, FORWARD);

  analogWrite(MOTOR_L_PWM_PIN, speed);
  analogWrite(MOTOR_R_PWM_PIN, speed);

  delay(del);

  //not sure how to make it stop so i'm just setitng the pins to 0

  analogWrite(MOTOR_L_PWM_PIN, 0);
  analogWrite(MOTOR_R_PWM_PIN, 0);

}

//turn left in place for a set time
void left(int del){
  digitalWrite(MOTOR_L_DIR_PIN, FORWARD);
  digitalWrite(MOTOR_R_DIR_PIN, REVERSE);

  //I thought it would be better to use a value that was high so the turn rate is less dependent on time as
  //the wheel accelerates faster
  analogWrite(MOTOR_L_PWM_PIN, 60);
  analogWrite(MOTOR_R_PWM_PIN, 60);

  delay(del);
  //not sure how to make it stop so i'm just setitng the pins to 0

  analogWrite(MOTOR_L_PWM_PIN, 0);
  analogWrite(MOTOR_R_PWM_PIN, 0);

}

//turn right in place for a set time
void right(int del){
  digitalWrite(MOTOR_L_DIR_PIN, REVERSE);
  digitalWrite(MOTOR_R_DIR_PIN, FORWARD);

  //I thought it would be better to use a value that was high so the turn rate is less dependent on time as
  //the wheel accelerates faster
  analogWrite(MOTOR_L_PWM_PIN, 60);
  analogWrite(MOTOR_R_PWM_PIN, 60);

  delay(del);
  //not sure how to make it stop so i'm just setitng the pins to 0

  analogWrite(MOTOR_L_PWM_PIN, 0);
  analogWrite(MOTOR_R_PWM_PIN, 0);

}
void loop() {
  // put your main code here, to run repeatedly:

}
