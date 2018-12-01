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

//IR sensors
#define IRLED1 65     //P7_0
#define IRLED2 48     //P7_1
#define IRLED3 64     //P7_2
#define IRLED4 47     //P7_3
#define IRLED5 52     //P7_4
#define IRLED6 68     //P7_5
#define IRLED7 53     //P7_6
#define IRLED8 69     //P7_7
#define LED_ON_PIN 61 //P5_3

//PID proportional control constant
#define KP 30

uint8_t LED_READ_POS = 0;

/********************
 * Value Definitions*
 ********************/

#define leftBase 70; //calibrated straight line drive speed, left motor
#define rightBase 70; //calibrated straight line drive speed, right motor

uint8_t LED_value [8] = {0,0,0,0,0,0,0,0};

#define FORWARD LOW
#define REVERSE HIGH


/////////////////////////////////////////////////////////////

void setup() {

  //Motor setup
  
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

  //IR LED setup
  
  pinMode(LED_ON_PIN, OUTPUT);

  Serial.begin(9600);

  
}

void loop() {

  //read IR LED array data
  //turn on IR LEDs
  digitalWrite(LED_ON_PIN, HIGH);
  
  //set I/O lines to OUTPUT
  pinMode(IRLED1, OUTPUT);
  pinMode(IRLED2, OUTPUT);
  pinMode(IRLED3, OUTPUT);
  pinMode(IRLED4, OUTPUT);
  pinMode(IRLED5, OUTPUT);
  pinMode(IRLED6, OUTPUT);
  pinMode(IRLED7, OUTPUT);
  pinMode(IRLED8, OUTPUT);

  //drive I/O lines high
  digitalWrite(IRLED1, HIGH);
  digitalWrite(IRLED2, HIGH);
  digitalWrite(IRLED3, HIGH);
  digitalWrite(IRLED4, HIGH);
  digitalWrite(IRLED5, HIGH);
  digitalWrite(IRLED6, HIGH);
  digitalWrite(IRLED7, HIGH);
  digitalWrite(IRLED8, HIGH);

  //delay for IR sensor saturation
  delayMicroseconds(20);

  pinMode(IRLED1, INPUT);
  pinMode(IRLED2, INPUT);
  pinMode(IRLED3, INPUT);
  pinMode(IRLED4, INPUT);
  pinMode(IRLED5, INPUT);
  pinMode(IRLED6, INPUT);
  pinMode(IRLED7, INPUT);
  pinMode(IRLED8, INPUT);

  //wait 1 ms and measure LED values
  delay(1);
  
  LED_value[0] = digitalRead(IRLED1) << 7;
  LED_value[1] = digitalRead(IRLED2) << 6;
  LED_value[2] = digitalRead(IRLED3) << 5;
  LED_value[3] = digitalRead(IRLED4) << 4;
  LED_value[4] = digitalRead(IRLED5) << 3;
  LED_value[5] = digitalRead(IRLED6) << 2;
  LED_value[6] = digitalRead(IRLED7) << 1;
  LED_value[7] = digitalRead(IRLED8);

//  Serial.print(LED_value[0]); Serial.print(" ");
//  Serial.print(LED_value[1]); Serial.print(" ");
//  Serial.print(LED_value[2]); Serial.print(" ");
//  Serial.print(LED_value[3]); Serial.print(" ");
//  Serial.print(LED_value[4]); Serial.print(" ");
//  Serial.print(LED_value[5]); Serial.print(" ");
//  Serial.print(LED_value[6]); Serial.print(" ");
//  Serial.print(LED_value[7]); Serial.print(" ");


  //rate-limit IR LED data capture rate to 100 Hz, and save power
  
  delay(9);
  digitalWrite(LED_ON_PIN, LOW);

  LED_READ_POS = 0;

  int i = 0;

  while (LED_READ_POS == 0 && i < 8)
  {
    LED_READ_POS += LED_value[i];
    i++;
  }

  if (i < 8)
  {
    LED_READ_POS -= LED_value[i];
  }
  
  //Serial.println(LED_READ_POS);

  int8_t delta = 0;
  if (LED_READ_POS == 16 || LED_READ_POS == 0)
  {
    //delta is 0
  }
  if (LED_READ_POS > 16)
  {
    i = LED_READ_POS;
    while (i != 16)
    {
      delta-=1;
      i>>=1;
    }
  }
  else
  {
    i = 16;
    while (i != LED_READ_POS)
    {
      delta+=1;
      i>>=1;
    }
  }

  int leftSpeed = leftBase;
  int rightSpeed = rightBase;

  if (delta < 0)
  {
    leftSpeed -= KP * delta;
  }
  else if (delta > 0)
  {
    rightSpeed += KP * delta;
  }
  
  constrain(leftSpeed, 30, 170);
  constrain(rightSpeed, 30, 170);
  
  analogWrite(MOTOR_L_PWM_PIN, leftSpeed);
  analogWrite(MOTOR_R_PWM_PIN, rightSpeed);

  Serial.print(delta); Serial.print(" ");
  Serial.print(leftSpeed); Serial.print(" ");
  Serial.println(rightSpeed); 

  delay(25);

}
