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

void loop() {
  // put your main code here, to run repeatedly:

}
