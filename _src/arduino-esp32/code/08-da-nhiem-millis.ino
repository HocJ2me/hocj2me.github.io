// Bài 8 – Làm nhiều việc "cùng lúc" bằng millis() (không dùng delay):
//   • LED trạng thái nháy mỗi 250 ms   • đọc cảm biến mỗi 1000 ms   • nút nhấn đổi chế độ phản hồi NGAY
//   • Máy trạng thái (state machine) cho 3 chế độ: TẮT -> TỰ ĐỘNG -> BẬT -> TẮT ...
const int LED_TT = 2, NUT = 0, QUAT = 26, CHAN_NHIET = 34;

enum CheDo { TAT, TU_DONG, BAT };
CheDo cheDo = TU_DONG;
const char* TEN_CHE_DO[] = {"TẮT", "TỰ ĐỘNG", "BẬT"};

unsigned long lanNhay = 0, lanDoc = 0, lanNhan = 0;
bool led = false;
int nutTruoc = HIGH;

void capNhatQuat(float nhietDo) {
  bool bat = (cheDo == BAT) || (cheDo == TU_DONG && nhietDo > 30);
  digitalWrite(QUAT, bat);
}

void setup() {
  pinMode(LED_TT, OUTPUT);
  pinMode(QUAT, OUTPUT);
  pinMode(NUT, INPUT_PULLUP);
  Serial.begin(115200);
}

void loop() {
  unsigned long now = millis();

  // Việc 1: nháy LED trạng thái
  if (now - lanNhay >= 250) {
    lanNhay = now;
    led = !led;
    digitalWrite(LED_TT, led);
  }

  // Việc 2: đọc cảm biến mỗi giây
  if (now - lanDoc >= 1000) {
    lanDoc = now;
    float nhietDo = analogRead(CHAN_NHIET) / 4095.0 * 50;     // giả sử cảm biến 0..50°C
    Serial.printf("[%lu] %.1f°C, chế độ %s\n", now, nhietDo, TEN_CHE_DO[cheDo]);
    capNhatQuat(nhietDo);
  }

  // Việc 3: nút nhấn (có chống dội 50 ms) đổi chế độ
  int nut = digitalRead(NUT);
  if (nut == LOW && nutTruoc == HIGH && now - lanNhan > 50) {
    lanNhan = now;
    cheDo = (CheDo)((cheDo + 1) % 3);
    Serial.printf("[%lu] Nút -> chế độ %s\n", now, TEN_CHE_DO[cheDo]);
  }
  nutTruoc = nut;
}
