// Bài 4 – Ngõ vào analog: quang trở (LDR) làm đèn ngủ tự động, biến trở chỉnh ngưỡng.
// ESP32: ADC 12 bit (0..4095) ở 3.3 V.  Arduino Uno: ADC 10 bit (0..1023) ở 5 V.
const int CHAN_LDR = 34;          // cầu phân áp: 3V3 – LDR – chân 34 – điện trở 10k – GND (tối -> giá trị nhỏ)
const int CHAN_BIEN_TRO = 35;     // chân giữa biến trở
const int DEN = 2;

void setup() {
  pinMode(DEN, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  int anhSang = analogRead(CHAN_LDR);
  int nguong = analogRead(CHAN_BIEN_TRO);
  float dienAp = anhSang * 3.3 / 4095;               // đổi giá trị ADC ra volt
  int phanTram = map(anhSang, 0, 4095, 0, 100);

  Serial.printf("Ánh sáng: %4d (%.2f V, %3d%%)  ngưỡng: %4d -> ", anhSang, dienAp, phanTram, nguong);
  if (anhSang < nguong) {
    digitalWrite(DEN, HIGH);
    Serial.println("TỐI, bật đèn");
  } else {
    digitalWrite(DEN, LOW);
    Serial.println("SÁNG, tắt đèn");
  }
  delay(500);
}
