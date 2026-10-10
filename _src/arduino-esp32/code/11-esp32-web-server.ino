// Bài 11 – ESP32 kết nối WiFi và làm WEB SERVER: mở trình duyệt trên điện thoại (cùng WiFi) để bật/tắt đèn, xem nhiệt độ.
#include <WiFi.h>
#include <WebServer.h>

const char* TEN_WIFI = "BKSTAR-Lab";
const char* MAT_KHAU = "12345678";
const int DEN = 2;
const int CHAN_NHIET = 34;

WebServer server(80);

void trangChu() {
  String html = "<h1>Nha thong minh</h1>";
  html += "<p>Den: " + String(digitalRead(DEN) ? "BAT" : "TAT") + "</p>";
  html += "<a href='/den?bat=1'>Bat</a> | <a href='/den?bat=0'>Tat</a>";
  server.send(200, "text/html", html);
}

void dieuKhienDen() {
  if (server.hasArg("bat")) digitalWrite(DEN, server.arg("bat") == "1" ? HIGH : LOW);
  server.send(200, "text/plain", digitalRead(DEN) ? "Den da BAT" : "Den da TAT");
}

void docNhietDo() {                     // trả về JSON cho app / trang web đọc
  float t = analogRead(CHAN_NHIET) / 4095.0 * 50;
  server.send(200, "application/json", "{\"nhiet_do\":" + String(t, 1) + "}");
}

void setup() {
  Serial.begin(115200);
  pinMode(DEN, OUTPUT);
  WiFi.mode(WIFI_STA);
  WiFi.begin(TEN_WIFI, MAT_KHAU);
  Serial.print("Đang kết nối WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Đã kết nối! Mở trình duyệt: http://");
  Serial.println(WiFi.localIP());

  server.on("/", trangChu);
  server.on("/den", dieuKhienDen);
  server.on("/nhiet-do", docNhietDo);
  server.onNotFound([] { server.send(404, "text/plain", "Khong co trang nay"); });
  server.begin();
}

void loop() {
  server.handleClient();               // phải gọi liên tục để phục vụ trình duyệt
}
