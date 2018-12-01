#include <cs117_swarmbot_library.h>

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

void loop() {
  // put your main code here, to run repeatedly: 
  
}
