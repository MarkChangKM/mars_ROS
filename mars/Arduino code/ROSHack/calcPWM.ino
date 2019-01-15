const int PWM_LOW = 60;
const int PWM_HIGH = 255;
int calcPWM(float v){
  int ans = floor(fabs(v) * (PWM_HIGH - PWM_LOW) + PWM_LOW);
  return min(PWM_HIGH, ans);
}

