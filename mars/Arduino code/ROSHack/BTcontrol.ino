void go()
{
  digitalWrite(AIN1, HIGH);
  digitalWrite(AIN2, LOW);
  digitalWrite(BIN1, HIGH);
  digitalWrite(BIN2, LOW);
  analogWrite(PWMA, BTspeed);
  analogWrite(PWMB, BTspeed);
  digitalWrite(STBY, HIGH);
}
void left()
{
  digitalWrite(AIN1, LOW);
  digitalWrite(AIN2, HIGH);
  digitalWrite(BIN1, HIGH);
  digitalWrite(BIN2, LOW);
  analogWrite(PWMA, BTspeed);
  analogWrite(PWMB, BTspeed);
  digitalWrite(STBY, HIGH);
}
void right()
{
  digitalWrite(AIN1, HIGH);
  digitalWrite(AIN2, LOW);
  digitalWrite(BIN1, LOW);
  digitalWrite(BIN2, HIGH);
  analogWrite(PWMA, BTspeed);
  analogWrite(PWMB, BTspeed);
  digitalWrite(STBY, HIGH);
}
void back()
{
  digitalWrite(AIN1, LOW);
  digitalWrite(AIN2, HIGH);
  digitalWrite(BIN1, LOW);
  digitalWrite(BIN2, HIGH);
  analogWrite(PWMA, BTspeed);
  analogWrite(PWMB, BTspeed);
  digitalWrite(STBY, HIGH);
}
void park()
{
  digitalWrite(STBY, LOW);
}
