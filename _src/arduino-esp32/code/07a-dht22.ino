// Bài 7 – Cảm biến nhiệt độ, độ ẩm DHT22: bật quạt khi nóng, cảnh báo khi độ ẩm cao.
// Thư viện: "DHT sensor library" (Adafruit). DHT22 đọc tối đa 1 lần / 2 giây.
#include <DHT.h>

const int CHAN_DHT = 4;
const int QUAT = 26;
DHT dht(CHAN_DHT, DHT22);

void setup() {
  Serial.begin(115200);
  dht.begin();
  pinMode(QUAT, OUTPUT);
}

void loop() {
  float t = dht.readTemperature();
  float h = dht.readHumidity();
  if (isnan(t) || isnan(h)) {                    // luôn kiểm tra: cảm biến lỏng dây sẽ trả về NaN
    Serial.println("Lỗi đọc DHT22!");
  } else {
    Serial.printf("Nhiệt độ: %.1f°C  Độ ẩm: %.1f%%\n", t, h);
    digitalWrite(QUAT, t >= 30 ? HIGH : LOW);
    if (h >= 80) Serial.println("  ! Độ ẩm cao – nguy cơ nấm mốc");
  }
  delay(2000);
}
