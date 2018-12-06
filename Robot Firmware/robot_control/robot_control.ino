#include <cs117_swarmbot_library.h>
#include <string.h>
#define forward_straight_cal_delay 100
#define reverse_straight_cal_delay 100
#define right_45_cal_delay 290
#define left_45_cal_delay 290

char rID[6] = "revaz";
int xCom = 0;
int yCom = 0;
int thetaCom = 0;

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

void move_forward(int move_time){
  digitalWrite(MOTOR_L_DIR_PIN, FORWARD);
  digitalWrite(MOTOR_R_DIR_PIN, FORWARD);

  analogWrite(MOTOR_L_PWM_PIN, STRAIGHT_DRIVE_SPEED);
  analogWrite(MOTOR_R_PWM_PIN, STRAIGHT_DRIVE_SPEED);

  delay(move_time); // delay_time specified in milliseconds

  analogWrite(MOTOR_L_PWM_PIN, 0);
  analogWrite(MOTOR_R_PWM_PIN, 0);

}

void move_backward(int move_time)
{
  digitalWrite(MOTOR_L_DIR_PIN, REVERSE);
  digitalWrite(MOTOR_R_DIR_PIN, REVERSE);

  analogWrite(MOTOR_L_PWM_PIN, STRAIGHT_DRIVE_SPEED);
  analogWrite(MOTOR_R_PWM_PIN, STRAIGHT_DRIVE_SPEED);

  delay(move_time); // delay_time specified in milliseconds

  analogWrite(MOTOR_L_PWM_PIN, 0);
  analogWrite(MOTOR_R_PWM_PIN, 0);
}


//calibration to turn right for 45 degrees
void turn_right(int turn_time){
  digitalWrite(MOTOR_L_DIR_PIN, FORWARD);
  digitalWrite(MOTOR_R_DIR_PIN, REVERSE);

  analogWrite(MOTOR_L_PWM_PIN, TURN_SPEED);
  analogWrite(MOTOR_R_PWM_PIN, TURN_SPEED);

  delay(turn_time);

  analogWrite(MOTOR_L_PWM_PIN, 0);
  analogWrite(MOTOR_R_PWM_PIN, 0);

}

//calibration to turn left for 45 degrees
void turn_left(int turn_time){
  digitalWrite(MOTOR_L_DIR_PIN, REVERSE);
  digitalWrite(MOTOR_R_DIR_PIN, FORWARD);

  analogWrite(MOTOR_L_PWM_PIN, TURN_SPEED);
  analogWrite(MOTOR_R_PWM_PIN, TURN_SPEED);

  delay(turn_time);

  analogWrite(MOTOR_L_PWM_PIN, 0);
  analogWrite(MOTOR_R_PWM_PIN, 0);

}

// takes a command string, interprets
int process_command(char* command){
  // go to first command in string
//  Serial.println("entered process_command");
  char* startCom = (char*) memchr(command,'<',strlen(command));
  char* token = strtok(startCom, " ");
  token = strtok(NULL, " ");

  // check id
  
  if(memcmp(token, rID, strlen(rID)) != 0){
    return 0;
  }
  
//  Serial.println("name match");
  //store dx, dy, theta
   token = strtok(NULL, " ");
   xCom = atoi(token);

   //store dx, dy, theta
   token = strtok(NULL, " ");
   yCom = atoi(token);

   //store dx, dy, theta
   token = strtok(NULL, " ");
   thetaCom = atoi(token);

   return 1;
}



void loop() {

  char str[50] = {'\0'};

  int available_bytes = Serial1.available();
  if (available_bytes > 0)
  {
    char readChar = Serial1.readBytesUntil('>', str, 500); 

    if (process_command(str) == 1)
    {
      int x_millis = xCom * pixels_to_millis;
      int y_millis = yCom * pixels_to_millis;
      int theta_millis = (int) ((((double) thetaCom) / 45) * turn_45_millis);

      // turning
      if (theta_millis < 0)
      {
        turn_right(abs(theta_millis));
      }
      else if (theta_millis > 0)
      {
        turn_left(theta_millis);
      }

      //movement along x

      if (x_millis < 0)
      {
        move_backward(abs(x_millis));
      }
      else if (x_millis > 0)
      {
        move_forward(x_millis);
      }

      //turn to face y and move along y

      if (y_millis > 0 )
      {
        turn_right (2 * turn_45_millis);
        move_forward(y_millis);
      }
      else if (y_millis < 0)
      {
        turn_left (2 * turn_45_millis);
        move_forward(abs(y_millis));
      }

      Serial1.write("< done >");

      
    }

  }

}
