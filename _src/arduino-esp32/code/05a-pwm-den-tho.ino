// Bài 5 – PWM: LED "thở" (sáng dần – tối dần).
// Arduino Uno: analogWrite(chân ~PWM, 0..255).   ESP32 (core 3.x): ledcAttach + ledcWrite.
const int LED = 9;

void setup() {
  pinMode(LED, OUTPUT);
}

void loop() {
  for (int doSang = 0; doSang <= 255; doSang += 51) {     // sáng dần
    analogWrite(LED, doSang);
    delay(100);
  }
  for (int doSang = 255; doSang >= 0; doSang -= 51) {     // tối dần
    analogWrite(LED, doSang);
    delay(100);
  }
}
