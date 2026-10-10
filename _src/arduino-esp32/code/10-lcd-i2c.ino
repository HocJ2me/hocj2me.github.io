// Bài 10 – Giao tiếp I2C: quét thiết bị trên bus, hiển thị lên màn hình LCD 16x2 (module I2C PCF8574).
// ESP32: SDA = GPIO 21, SCL = GPIO 22.  Arduino Uno: SDA = A4, SCL = A5.
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);    // địa chỉ 0x27 (có module là 0x3F)
DHT dht(4, DHT22);

void quetI2C() {
  Serial.println("Quét bus I2C...");
  for (uint8_t dc = 1; dc < 127; dc++) {
    Wire.beginTransmission(dc);
    if (Wire.endTransmission() == 0) Serial.printf("  tìm thấy thiết bị tại 0x%02X\n", dc);
  }
}

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);
  quetI2C();
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Tram thoi tiet");
  lcd.setCursor(0, 1);
  lcd.print("BKSTAR v1.0");
  dht.begin();
  delay(1500);
}

void loop() {
  float t = dht.readTemperature();
  float h = dht.readHumidity();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Nhiet do: ");
  lcd.print(t, 1);
  lcd.print("C");
  lcd.setCursor(0, 1);
  lcd.print("Do am   : ");
  lcd.print(h, 0);
  lcd.print("%");
  delay(2000);
}
