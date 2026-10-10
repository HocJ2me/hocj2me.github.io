// Bài 2 – Đèn giao thông: 3 LED đỏ / vàng / xanh, mỗi LED nối nối tiếp một điện trở 220 Ω xuống GND.
const int DEN_DO = 4;
const int DEN_VANG = 5;
const int DEN_XANH = 6;

// Hàm phụ: bật đúng một đèn, tắt hai đèn còn lại
void batDen(int den) {
  digitalWrite(DEN_DO,   den == DEN_DO   ? HIGH : LOW);
  digitalWrite(DEN_VANG, den == DEN_VANG ? HIGH : LOW);
  digitalWrite(DEN_XANH, den == DEN_XANH ? HIGH : LOW);
}

void setup() {
  pinMode(DEN_DO, OUTPUT);
  pinMode(DEN_VANG, OUTPUT);
  pinMode(DEN_XANH, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  Serial.println("XANH: được đi");
  batDen(DEN_XANH);
  delay(3000);

  Serial.println("VÀNG: chuẩn bị dừng");
  batDen(DEN_VANG);
  delay(1000);

  Serial.println("ĐỎ: dừng lại");
  batDen(DEN_DO);
  delay(3000);
}
