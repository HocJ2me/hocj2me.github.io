// Bài 7 – Cảm biến siêu âm HC-SR04: đo khoảng cách, còi kêu nhanh dần khi vật cản tới gần (cảm biến lùi xe).
const int TRIG = 5;
const int ECHO = 18;      // ESP32 3.3 V: dùng HC-SR04P (3.3 V) hoặc cầu phân áp cho chân ECHO
const int COI = 19;

float docKhoangCachCm() {
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);              // xung kích 10 µs
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  unsigned long thoiGian = pulseIn(ECHO, HIGH, 30000);   // thời gian sóng đi và về (µs)
  if (thoiGian == 0) return -1;          // không nhận được tiếng vọng
  return thoiGian * 0.0343 / 2;          // vận tốc âm thanh 343 m/s = 0.0343 cm/µs, chia 2 vì đi - về
}

void setup() {
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
  Serial.begin(115200);
}

void loop() {
  float d = docKhoangCachCm();
  if (d < 0) {
    Serial.println("Ngoài tầm đo");
  } else if (d < 10) {
    Serial.printf("%.1f cm – DỪNG LẠI!\n", d);
    tone(COI, 2000);
  } else if (d < 40) {
    Serial.printf("%.1f cm – gần\n", d);
    tone(COI, 1000, 100);
  } else {
    Serial.printf("%.1f cm – an toàn\n", d);
    noTone(COI);
  }
  delay(300);
}
