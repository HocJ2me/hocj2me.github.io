// Bài 9 – Ngắt ngoài (interrupt): đếm xung encoder bánh xe để tính tốc độ, không bỏ sót xung dù loop() bận.
const int CHAN_ENCODER = 27;
const int XUNG_MOI_VONG = 20;          // đĩa encoder 20 lỗ
const float CHU_VI_BANH_CM = 20.4;     // bánh xe đường kính 6.5 cm

volatile unsigned long demXung = 0;    // volatile: biến dùng chung giữa ISR và loop()

void IRAM_ATTR khiCoXung() {           // ISR: thật ngắn – chỉ đếm
  demXung++;
}

void setup() {
  Serial.begin(115200);
  pinMode(CHAN_ENCODER, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(CHAN_ENCODER), khiCoXung, RISING);
}

void loop() {
  static unsigned long xungTruoc = 0;
  delay(500);                          // loop() làm việc khác 500 ms – ngắt vẫn đếm đủ
  noInterrupts();                      // đọc biến chung an toàn
  unsigned long xung = demXung;
  interrupts();
  unsigned long moi = xung - xungTruoc;
  xungTruoc = xung;
  float vongPhut = moi / (float)XUNG_MOI_VONG / 0.5 * 60;
  float cmGiay = moi / (float)XUNG_MOI_VONG * CHU_VI_BANH_CM / 0.5;
  Serial.printf("%3lu xung/0.5s -> %5.1f vòng/phút, %5.1f cm/s (tổng %lu xung)\n", moi, vongPhut, cmGiay, xung);
}
