#include <cs117_swarmbot_library.h>
#define 
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

//The idea is to move forward for a set time and then based on the amount that's reported as moved,
//we normalize the speed terms
void forward_cal(){
  digitalWrite(MOTOR_L_DIR_PIN, FORWARD);
  digitalWrite(MOTOR_R_DIR_PIN, FORWARD);

  analogWrite(MOTOR_L_PWM_PIN, 65);
  analogWrite(MOTOR_R_PWM_PIN, 65);

  delay(del);

  //not sure how to make it stop so i'm just setitng the pins to 0

  analogWrite(MOTOR_L_PWM_PIN, 0);
  analogWrite(MOTOR_R_PWM_PIN, 0);

}

void loop() {
  // put your main code here, to run repeatedly: 
  
}
