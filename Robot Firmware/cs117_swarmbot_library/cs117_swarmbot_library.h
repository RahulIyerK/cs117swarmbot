#ifndef CS117_SWARMBOT
#define CS117_SWARMBOT
/******************
 * Pin Definitions*
 ******************/

//Right Motor
#define MOTOR_L_DIR_PIN 14 //P1.7
#define MOTOR_L_PWM_PIN 40 //P2.7
#define MOTOR_L_SLP_PIN 31 //P3.7

//Left Motor
#define MOTOR_R_DIR_PIN 15 //P1.6
#define MOTOR_R_PWM_PIN 39 //P2.6
#define MOTOR_R_SLP_PIN 11 //P3.6

/********************
 * Drive Directions *
 ********************/

#define FORWARD LOW
#define REVERSE HIGH

/*******************
 * Drive Constants *
 *******************/

#define STRAIGHT_DRIVE_SPEED 50
#define TURN_SPEED 60

#define pixels_to_millis 20

#define turn_45_millis 290

#endif
