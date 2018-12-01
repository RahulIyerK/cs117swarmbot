#include <cs117_swarmbot_library.h>
#define forward_straight_cal_delay 100
#define reverse_straight_cal_delay 100
#define right_45_cal_delay 290
#define left_45_cal_delay 290


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

  Serial1.begin(9600);
}

//The idea is to move straight forward for a set period of time and stop.
//This allows us to calibrate the delay_time to the approximate distance moved.
void forward_cal(){
  digitalWrite(MOTOR_L_DIR_PIN, FORWARD);
  digitalWrite(MOTOR_R_DIR_PIN, FORWARD);

  analogWrite(MOTOR_L_PWM_PIN, MOTOR_L_STRAIGHT_FORWARD_PWM);
  analogWrite(MOTOR_R_PWM_PIN, MOTOR_R_STRAIGHT_FORWARD_PWM);

  delay(forward_straight_cal_delay); // delay_time specified in milliseconds

  analogWrite(MOTOR_L_PWM_PIN, 0);
  analogWrite(MOTOR_R_PWM_PIN, 0);

}

void reverse_cal()
{
  digitalWrite(MOTOR_L_DIR_PIN, REVERSE);
  digitalWrite(MOTOR_R_DIR_PIN, REVERSE);

  analogWrite(MOTOR_L_PWM_PIN, MOTOR_L_STRAIGHT_REVERSE_PWM);
  analogWrite(MOTOR_R_PWM_PIN, MOTOR_R_STRAIGHT_REVERSE_PWM);

  delay(reverse_straight_cal_delay); // delay_time specified in milliseconds

  analogWrite(MOTOR_L_PWM_PIN, 0);
  analogWrite(MOTOR_R_PWM_PIN, 0);
}


//calibration to turn right for 45 degrees
void right_cal(){
  digitalWrite(MOTOR_L_DIR_PIN, FORWARD);
  digitalWrite(MOTOR_R_DIR_PIN, REVERSE);

  analogWrite(MOTOR_L_PWM_PIN, 60);
  analogWrite(MOTOR_R_PWM_PIN, 60);

  delay(right_45_cal_delay);

  analogWrite(MOTOR_L_PWM_PIN, 0);
  analogWrite(MOTOR_R_PWM_PIN, 0);

}

//calibration to turn left for 45 degrees
void left_cal(){
  digitalWrite(MOTOR_L_DIR_PIN, REVERSE);
  digitalWrite(MOTOR_R_DIR_PIN, FORWARD);

  analogWrite(MOTOR_L_PWM_PIN, 60);
  analogWrite(MOTOR_R_PWM_PIN, 60);

  delay(left_45_cal_delay);

  analogWrite(MOTOR_L_PWM_PIN, 0);
  analogWrite(MOTOR_R_PWM_PIN, 0);

}



void loop() {
//  Serial1.write("write tomat\n");
//  forward_cal();
//  reverse_cal();
//  right_cal();
  left_cal();
  delay(2000);

}
