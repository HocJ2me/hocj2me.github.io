// Bài 6 – Giao tiếp Serial: nhận lệnh văn bản từ máy tính / app Bluetooth để điều khiển thiết bị.
// Mở Serial Monitor (115200, kết thúc dòng: Newline) rồi gõ: LED ON, LED OFF, PWM 128, STATUS
const int LED = 2;
const int QUAT = 25;
int tocDoQuat = 0;

void xuLyLenh(String lenh) {
  lenh.trim();
  lenh.toUpperCase();
  if (lenh == "LED ON") {
    digitalWrite(LED, HIGH);
    Serial.println("OK: đèn bật");
  } else if (lenh == "LED OFF") {
    digitalWrite(LED, LOW);
    Serial.println("OK: đèn tắt");
  } else if (lenh.startsWith("PWM ")) {
    tocDoQuat = constrain(lenh.substring(4).toInt(), 0, 255);
    analogWrite(QUAT, tocDoQuat);
    Serial.printf("OK: quạt = %d\n", tocDoQuat);
  } else if (lenh == "STATUS") {
    Serial.printf("Đèn: %s, quạt: %d, chạy được %lu ms\n", digitalRead(LED) ? "bật" : "tắt", tocDoQuat, millis());
  } else {
    Serial.println("Lỗi: không hiểu lệnh \"" + lenh + "\"");
  }
}

void setup() {
  pinMode(LED, OUTPUT);
  Serial.begin(115200);
  Serial.println("Sẵn sàng nhận lệnh: LED ON | LED OFF | PWM <0-255> | STATUS");
}

void loop() {
  if (Serial.available()) {                       // có dữ liệu đang chờ trong bộ đệm
    String lenh = Serial.readStringUntil('\n');   // đọc tới hết dòng
    Serial.print("> ");
    Serial.println(lenh);
    xuLyLenh(lenh);
  }
}
