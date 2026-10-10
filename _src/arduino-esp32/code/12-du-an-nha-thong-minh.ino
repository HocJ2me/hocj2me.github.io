// Bài 12 – DỰ ÁN: Nhà thông minh IoT với ESP32 + MQTT
//   • Gửi nhiệt độ, độ ẩm, ánh sáng lên broker MQTT mỗi 2 giây (app điện thoại / Node-RED / Home Assistant hiển thị)
//   • Nhận lệnh bật/tắt đèn, quạt từ app qua topic nha/dieu-khien
//   • Tự động: tối thì bật đèn hiên, nóng quá thì bật quạt (khi đang ở chế độ tự động)
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

const int DEN_HIEN = 2, QUAT = 26, CHAN_LDR = 34;
DHT dht(4, DHT22);
WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);
bool tuDong = true;
unsigned long lanGui = 0;

void khiNhanTin(char* topic, byte* duLieu, unsigned int len) {
  String lenh = "";
  for (unsigned int i = 0; i < len; i++) lenh += (char)duLieu[i];
  if (lenh == "den:bat") digitalWrite(DEN_HIEN, HIGH);
  else if (lenh == "den:tat") digitalWrite(DEN_HIEN, LOW);
  else if (lenh == "quat:bat") digitalWrite(QUAT, HIGH);
  else if (lenh == "quat:tat") digitalWrite(QUAT, LOW);
  else if (lenh == "che-do:tu-dong") tuDong = true;
  else if (lenh == "che-do:thu-cong") tuDong = false;
  Serial.printf("Lệnh \"%s\" -> chế độ %s\n", lenh.c_str(), tuDong ? "tự động" : "thủ công");
  (void)topic;
}

void ketNoi() {
  WiFi.begin("BKSTAR-Lab", "12345678");
  while (WiFi.status() != WL_CONNECTED) delay(250);
  Serial.println("WiFi OK, IP " + WiFi.localIP());
  mqtt.setServer("broker.hivemq.com", 1883);
  mqtt.setCallback(khiNhanTin);
  mqtt.connect("bkstar-nha-01");
  mqtt.subscribe("nha/dieu-khien");
}

void setup() {
  Serial.begin(115200);
  pinMode(DEN_HIEN, OUTPUT);
  pinMode(QUAT, OUTPUT);
  dht.begin();
  ketNoi();
}

void loop() {
  mqtt.loop();                                   // nhận tin MQTT
  if (millis() - lanGui >= 2000) {
    lanGui = millis();
    float t = dht.readTemperature(), h = dht.readHumidity();
    int anhSang = analogRead(CHAN_LDR);
    char json[96];
    snprintf(json, sizeof json, "{\"t\":%.1f,\"h\":%.0f,\"anh_sang\":%d}", t, h, anhSang);
    mqtt.publish("nha/cam-bien", json);
    if (tuDong) {
      digitalWrite(DEN_HIEN, anhSang < 1200);
      digitalWrite(QUAT, t > 31);
    }
  }
}
