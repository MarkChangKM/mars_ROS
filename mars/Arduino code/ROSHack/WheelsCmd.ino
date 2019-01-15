void WheelsCmd(const duckietown_msgs::WheelsCmdStamped& cmd_msg)
{
  digitalWrite(STBY, HIGH);
  vel_left = calcPWM(cmd_msg.vel_left);
  vel_right = calcPWM(cmd_msg.vel_right);
  if(cmd_msg.vel_left == 0)
    vel_left = 0;
  else if(cmd_msg.vel_left > 0)
  {
    digitalWrite(AIN1, HIGH);
    digitalWrite(AIN2, LOW);
  }
  else
  {
    digitalWrite(AIN1, LOW);
    digitalWrite(AIN2, HIGH);
  }
  if(cmd_msg.vel_right == 0)
    vel_right = 0;
  else if(cmd_msg.vel_right > 0)
  {
    digitalWrite(BIN1, HIGH);
    digitalWrite(BIN2, LOW);
  }
  else
  {
    digitalWrite(BIN1, LOW);
    digitalWrite(BIN2, HIGH);
  }
  analogWrite(PWMA, vel_left);
  analogWrite(PWMB, vel_right);
}
