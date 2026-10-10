// Mô phỏng các thư viện thiết bị hay dùng: Servo, DHT, LiquidCrystal_I2C, Wire, WiFi, WebServer, PubSubClient (MQTT)
#pragma once
#include "Arduino.h"

// ----------------------------------------------------------------- Servo
class Servo {
public:
    void attach(int pin) { pin_ = pin; }
    void write(int goc) {
        goc = constrain(goc, 0, 180);
        if (goc != goc_) { goc_ = goc; sim::event("Servo %s quay tới %d°", sim::pin_name(pin_).c_str(), goc); }
    }
    int read() const { return goc_; }
private:
    int pin_ = -1, goc_ = -1;
};

// ----------------------------------------------------------------- DHT11 / DHT22
#define DHT11 11
#define DHT22 22
inline std::function<float(uint32_t)> sim_dht_nhiet = [](uint32_t) { return 28.0f; };
inline std::function<float(uint32_t)> sim_dht_am = [](uint32_t) { return 60.0f; };
class DHT {
public:
    DHT(int pin, int type) : pin_(pin), type_(type) {}
    void begin() {}
    float readTemperature() { return std::round(sim_dht_nhiet(sim::ms()) * 10) / 10; }
    float readHumidity() { return std::round(sim_dht_am(sim::ms()) * 10) / 10; }
private:
    int pin_, type_;
};

// ----------------------------------------------------------------- Wire (I2C)
class SimWire {
public:
    void begin(int sda = -1, int scl = -1) { (void)sda; (void)scl; }
    void beginTransmission(uint8_t addr) { addr_ = addr; }
    uint8_t endTransmission() { for (int a : thiet_bi) if (a == addr_) return 0; return 2; }   // 0 = có thiết bị trả lời
    std::vector<int> thiet_bi = {0x27, 0x76};                                                  // LCD + BME280 trên bus
private:
    uint8_t addr_ = 0;
};
inline SimWire Wire;

// ----------------------------------------------------------------- LCD 16x2 I2C: in khung LCD mỗi khi nội dung đổi
class LiquidCrystal_I2C {
public:
    LiquidCrystal_I2C(uint8_t addr, int cols, int rows) : cols_(cols), rows_(rows) {
        (void)addr;
        clear_();
        sim::on_tick.push_back([this] { flush(); });
    }
    void init() {}
    void begin() {}
    void backlight() {}
    void clear() { clear_(); dirty_ = true; }
    void setCursor(int c, int r) { c_ = c; r_ = r; }
    template <class T> void print(const T& v) { put(String(v)); }
    void print(const char* s) { put(String(s)); }
    void print(float v, int dec) { put(String((double)v, dec)); }
    void print(double v, int dec) { put(String(v, dec)); }
    void flush() {
        if (!dirty_) return;
        dirty_ = false;
        std::string s = lines_[0] + "|" + lines_[1];
        if (s == last_) return;
        last_ = s;
        sim::event("LCD |%s|", lines_[0].c_str());
        std::printf("                       |%s|\n", lines_[1].c_str());
    }
private:
    int cols_, rows_, c_ = 0, r_ = 0;
    bool dirty_ = false;
    std::string lines_[2], last_;
    void clear_() { lines_[0] = lines_[1] = std::string(cols_, ' '); c_ = r_ = 0; }
    void put(const std::string& s) {
        for (char ch : s) { if (c_ < cols_ && r_ < 2) lines_[r_][c_++] = ch; }
        dirty_ = true;
    }
};

// ----------------------------------------------------------------- WiFi (ESP32)
#define WIFI_STA 1
#define WL_CONNECTED 3
#define WL_DISCONNECTED 6
class SimWiFi {
public:
    void mode(int) {}
    void begin(const char* ssid, const char* pass) { ssid_ = ssid; (void)pass; t0_ = sim::ms(); }
    int status() { return (!ssid_.empty() && sim::ms() - t0_ >= 1500) ? WL_CONNECTED : WL_DISCONNECTED; }
    String localIP() { return String("192.168.1.25"); }
    int RSSI() { return -58; }
private:
    std::string ssid_;
    uint32_t t0_ = 0;
};
inline SimWiFi WiFi;

// ----------------------------------------------------------------- WebServer (ESP32): yêu cầu HTTP theo kịch bản
class WebServer {
public:
    explicit WebServer(int port) { (void)port; }
    void on(const char* path, std::function<void()> h) { handlers_[path] = h; }
    void onNotFound(std::function<void()> h) { notfound_ = h; }
    void begin() {}
    void sim_yeu_cau(uint32_t t, const char* url) { sched_.push_back({t, url}); }
    void handleClient() {
        for (auto it = sched_.begin(); it != sched_.end(); ++it) {
            if (it->t <= sim::ms()) {
                std::string url = it->url;
                sched_.erase(it);
                auto q = url.find('?');
                uri_ = url.substr(0, q);
                args_.clear();
                if (q != std::string::npos) parse(url.substr(q + 1));
                sim::event("Trình duyệt gửi: GET %s", url.c_str());
                auto h = handlers_.find(uri_);
                if (h != handlers_.end()) h->second(); else if (notfound_) notfound_(); else send(404, "text/plain", "Not found");
                return;
            }
        }
    }
    String uri() { return String(uri_); }
    String arg(const char* name) { return String(args_[name]); }
    bool hasArg(const char* name) { return args_.count(name) > 0; }
    void send(int code, const char* type, const String& body) {
        std::string b = body;
        if (b.size() > 70) b = b.substr(0, 67) + "...";
        sim::event("Phản hồi %d (%s): %s", code, type, b.c_str());
    }
private:
    struct Req { uint32_t t; std::string url; };
    std::vector<Req> sched_;
    std::map<std::string, std::function<void()>> handlers_;
    std::function<void()> notfound_;
    std::string uri_;
    std::map<std::string, std::string> args_;
    void parse(const std::string& qs) {
        size_t a = 0;
        while (a < qs.size()) {
            size_t e = qs.find('&', a); if (e == std::string::npos) e = qs.size();
            std::string kv = qs.substr(a, e - a);
            size_t eq = kv.find('=');
            args_[kv.substr(0, eq)] = eq == std::string::npos ? "" : kv.substr(eq + 1);
            a = e + 1;
        }
    }
};

// ----------------------------------------------------------------- PubSubClient (MQTT)
class WiFiClient {};
class PubSubClient {
public:
    explicit PubSubClient(WiFiClient&) {}
    void setServer(const char* host, int port) { host_ = host; (void)port; }
    void setCallback(void (*cb)(char*, byte*, unsigned int)) { cb_ = cb; }
    bool connect(const char* id) { ok_ = true; sim::event("MQTT kết nối broker %s với id \"%s\"", host_.c_str(), id); return true; }
    bool connected() { return ok_; }
    bool subscribe(const char* topic) { sim::event("MQTT đăng ký nhận topic %s", topic); return true; }
    bool publish(const char* topic, const char* payload) { sim::event("MQTT gửi  %s = %s", topic, payload); return true; }
    void sim_tin_den(uint32_t t, const char* topic, const char* payload) { sched_.push_back({t, topic, payload}); }
    void loop() {
        for (auto it = sched_.begin(); it != sched_.end(); ++it) {
            if (it->t <= sim::ms()) {
                Msg m = *it; sched_.erase(it);
                sim::event("MQTT nhận %s = %s", m.topic.c_str(), m.payload.c_str());
                if (cb_) cb_((char*)m.topic.c_str(), (byte*)m.payload.data(), (unsigned)m.payload.size());
                return;
            }
        }
    }
private:
    struct Msg { uint32_t t; std::string topic, payload; };
    std::vector<Msg> sched_;
    std::string host_;
    bool ok_ = false;
    void (*cb_)(char*, byte*, unsigned int) = nullptr;
};
