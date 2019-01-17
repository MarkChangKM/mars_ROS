#include <SoftwareSerial.h>
#include <ros.h>
#include <duckietown_msgs/WheelsCmdStamped.h>
ros::NodeHandle nh;

int vel_left = 0;
int vel_right = 0;
int incomingByte = 4;

SoftwareSerial BTSerial(10,9);
#define SPEA 13
#define SPEB 3
#define STBY 6 //standby
//Motor A left
#define PWMA 11 //Speed control
#define AIN1 4  //Direction
#define AIN2 12 //Direction
//Motor B right
#define PWMB 5 //Speed control
#define BIN1 7 //Direction
#define BIN2 8 //Direction

#define BTspeed 60

void WheelsCmd(const duckietown_msgs::WheelsCmdStamped& cmd_msg);
ros::Subscriber<duckietown_msgs::WheelsCmdStamped> Wheelcmd("wheels_cmd_executed",WheelsCmd);

typedef void (*f)();
f func[5] = {&go, &left, &right, &back, &park};

void setup() {
  Init();  
}

void loop() {
  if (BTSerial.available())
    func[BTSerial.read()]();
  nh.spinOnce();
}
