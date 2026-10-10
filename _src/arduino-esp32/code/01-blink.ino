// Bài 1 – Blink: "Hello world" của vi điều khiển. Nháy LED có sẵn trên board mỗi 500 ms.
// Arduino Uno: LED_BUILTIN là chân 13.  ESP32 DevKit: LED xanh ở GPIO 2 (nếu board có LED).

void setup() {                       // chạy MỘT lần khi cấp điện hoặc nhấn reset
  pinMode(LED_BUILTIN, OUTPUT);      // khai báo chân là ngõ RA
  Serial.begin(115200);              // mở cổng Serial để in thông tin lên máy tính
  Serial.println("Board đã khởi động!");
}

void loop() {                        // lặp lại MÃI MÃI
  digitalWrite(LED_BUILTIN, HIGH);   // xuất mức cao (5 V / 3.3 V) -> LED sáng
  delay(500);                        // chờ 500 ms
  digitalWrite(LED_BUILTIN, LOW);    // xuất mức thấp (0 V) -> LED tắt
  delay(500);
}
