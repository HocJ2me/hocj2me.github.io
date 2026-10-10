// Bài 5 – Servo theo biến trở và điều tốc động cơ DC bằng PWM trên ESP32 (bộ LEDC)
#include <ESP32Servo.h>      // Arduino Uno dùng <Servo.h> – cách dùng giống hệt

const int CHAN_SERVO = 18;
const int CHAN_BIEN_TRO = 34;
const int CHAN_PWM_DONG_CO = 25;      // nối tới chân ENA của driver L298N / TB6612

Servo servo;

void setup() {
  Serial.begin(115200);
  servo.attach(CHAN_SERVO);
  ledcAttach(CHAN_PWM_DONG_CO, 20000, 8);   // tần số 20 kHz (không kêu rít), độ phân giải 8 bit: 0..255
}

void loop() {
  int bienTro = analogRead(CHAN_BIEN_TRO);          // 0..4095
  int goc = map(bienTro, 0, 4095, 0, 180);
  int tocDo = map(bienTro, 0, 4095, 0, 255);
  servo.write(goc);
  ledcWrite(CHAN_PWM_DONG_CO, tocDo);
  Serial.printf("biến trở %4d -> servo %3d°, động cơ %3d%%\n", bienTro, goc, tocDo * 100 / 255);
  delay(400);
}
