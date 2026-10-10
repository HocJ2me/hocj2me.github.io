#include "Arduino.h"
void sim_kich_ban() {
  sim_ten_chan(2, "đèn");
  sim_ten_chan(25, "quạt");
  Serial.sim_nhap(300, "LED ON\n");
  Serial.sim_nhap(800, "pwm 180\n");
  Serial.sim_nhap(1300, "STATUS\n");
  Serial.sim_nhap(1700, "MO CUA\n");
  Serial.sim_nhap(2100, "led off\n");
  sim_ket_thuc_sau(2400);
}
