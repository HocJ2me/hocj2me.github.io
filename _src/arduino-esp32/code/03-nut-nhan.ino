// Bài 3 – Nút nhấn: đọc ngõ vào số, điện trở kéo lên trong (INPUT_PULLUP), chống dội phím, bật/tắt LED.
// Nối: một chân nút vào chân 2, chân kia xuống GND.  Không nhấn = HIGH, nhấn = LOW.
const int NUT = 2;
const int LED = 13;
const unsigned long CHONG_DOI_MS = 30;

bool trangThaiLed = false;
int trangThaiOnDinh = HIGH;        // trạng thái nút đã được xác nhận
int lanDocTruoc = HIGH;
unsigned long lanDoiCuoi = 0;
int soLanNhan = 0;

void setup() {
  pinMode(NUT, INPUT_PULLUP);
  pinMode(LED, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  int doc = digitalRead(NUT);
  if (doc != lanDocTruoc) {         // tín hiệu vừa thay đổi (có thể do nảy tiếp điểm)
    lanDoiCuoi = millis();
    lanDocTruoc = doc;
  }
  // Chỉ tin trạng thái mới nếu nó giữ nguyên đủ 30 ms
  if (millis() - lanDoiCuoi > CHONG_DOI_MS && doc != trangThaiOnDinh) {
    trangThaiOnDinh = doc;
    if (trangThaiOnDinh == LOW) {   // cạnh xuống = vừa nhấn
      soLanNhan++;
      trangThaiLed = !trangThaiLed;
      digitalWrite(LED, trangThaiLed);
      Serial.print("Nhấn lần ");
      Serial.println(soLanNhan);
    }
  }
}
