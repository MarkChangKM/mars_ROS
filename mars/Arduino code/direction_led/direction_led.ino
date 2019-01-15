#include <ros.h>
#include <std_msgs/Bool.h>
ros::NodeHandle nh;

#define LEDR 13
#define LEDL 12

bool d;
std_msgs::Bool runA;

void dir(const std_msgs::Bool& cmd_msg)
{
  d=cmd_msg.data;
  if(d)
  {
    digitalWrite(LEDR,HIGH);
    digitalWrite(LEDL,LOW);
  }
  else
  {
    digitalWrite(LEDL,HIGH);
    digitalWrite(LEDR,LOW);
  }
}
ros::Subscriber<std_msgs::Bool> direct("direction", dir);

void setup() 
{
  pinMode(LEDR, OUTPUT);
  pinMode(LEDL, OUTPUT);
  nh.initNode();
  nh.subscribe(direct);
}

void loop() {
  nh.spinOnce();

}
