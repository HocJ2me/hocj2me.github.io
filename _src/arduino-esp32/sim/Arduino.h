// Arduino.h – BỘ MÔ PHỎNG Arduino/ESP32 trên máy tính (dùng cho khóa học, không phải thư viện thật).
// Sketch .ino được biên dịch bằng g++ cùng file này; thời gian là thời gian ẢO (delay() không chờ thật).
// In ra: dòng Serial như Serial Monitor, và dòng "⚡ [t ms] ..." khi trạng thái chân / thiết bị thay đổi.
#pragma once
#include <cmath>
#include <math.h>
#include <cstdarg>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <functional>
#include <map>
#include <string>
#include <vector>

typedef uint8_t byte;
typedef bool boolean;
#define HIGH 1
#define LOW 0
#define INPUT 0
#define OUTPUT 1
#define INPUT_PULLUP 2
#define CHANGE 1
#define FALLING 2
#define RISING 3
#ifndef LED_BUILTIN
#define LED_BUILTIN 13
#endif
#define A0 14
#define A1 15
#define A2 16
#define A3 17
#define digitalPinToInterrupt(p) (p)
#define PI 3.14159265358979

// ===================================================================== lõi mô phỏng
namespace sim {
inline uint64_t now_us = 0;
inline uint64_t end_ms = 3000;
inline uint32_t loop_us = 20;                   // mỗi lần loop() coi như tốn 20 µs
inline bool serial_open_line = false;
inline std::vector<std::string> pending;          // sự kiện chờ in sau khi dòng Serial hiện tại kết thúc
inline std::map<int, std::string> names;
inline std::map<int, int> mode, out, pwm;
inline std::map<int, std::function<int(uint32_t)>> din;   // chân vào số: hàm theo thời gian (ms)
inline std::map<int, std::function<int(uint32_t)>> ain;   // chân vào analog
inline std::map<int, std::function<uint32_t(uint32_t)>> pulse;
struct Isr { void (*fn)(); int mode; int last; };
inline std::map<int, Isr> isrs;
inline std::vector<std::function<void()>> on_tick;   // các thiết bị cần cập nhật theo thời gian
inline uint32_t ms() { return (uint32_t)(now_us / 1000); }
inline std::string pin_name(int p) {
    auto it = names.find(p);
    char b[16]; std::snprintf(b, sizeof b, "chân %d", p);
    return it != names.end() ? std::string(b) + " (" + it->second + ")" : std::string(b);
}
inline void event(const char* fmt, ...) {
    char msg[512];
    int n = std::snprintf(msg, sizeof msg, "   ⚡ [%5u ms] ", ms());
    va_list ap; va_start(ap, fmt); std::vsnprintf(msg + n, sizeof msg - n, fmt, ap); va_end(ap);
    if (serial_open_line) pending.push_back(msg);   // đang in dở một dòng Serial: in sau
    else std::printf("%s\n", msg);
}
inline void flush_pending() {
    for (auto& m : pending) std::printf("%s\n", m.c_str());
    pending.clear();
}
inline bool logged(int p) { return names.count(p) > 0; }    // chỉ ghi log các chân đã đặt tên trong kịch bản
inline int read_digital(int p) {
    auto it = din.find(p);
    if (it != din.end()) return it->second(ms()) ? HIGH : LOW;
    if (mode[p] == INPUT_PULLUP) return HIGH;
    if (mode[p] == OUTPUT) return out[p];
    return LOW;
}
inline void check_isr() {
    for (auto& [p, r] : isrs) {
        int v = read_digital(p);
        if (v != r.last) {
            bool fire = r.mode == CHANGE || (r.mode == RISING && v == HIGH) || (r.mode == FALLING && v == LOW);
            r.last = v;
            if (fire) r.fn();
        }
    }
}
inline void advance_us(uint64_t us) {             // cho thời gian trôi, kiểm tra ngắt từng 100 µs
    uint64_t target = now_us + us;
    while (now_us < target) {
        uint64_t step = std::min<uint64_t>(100, target - now_us);
        uint32_t before = ms();
        now_us += step;
        check_isr();
        if (ms() != before) {
            for (auto& f : on_tick) f();
            if (ms() >= end_ms) {                   // hết thời gian mô phỏng -> dừng ngay
                if (serial_open_line) std::printf("\n");
                flush_pending();
                std::printf("── hết mô phỏng tại %u ms ──\n", ms());
                std::fflush(stdout);
                std::exit(0);
            }
        }
    }
}
}  // namespace sim

// Các hàm cấu hình kịch bản (gọi trong sim_kich_ban())
inline void sim_ten_chan(int p, const char* ten) { sim::names[p] = ten; }
inline void sim_digital(int p, std::function<int(uint32_t)> f) { sim::din[p] = f; }
inline void sim_analog(int p, std::function<int(uint32_t)> f) { sim::ain[p] = f; }
inline void sim_pulse(int p, std::function<uint32_t(uint32_t)> f) { sim::pulse[p] = f; }
inline void sim_ket_thuc_sau(uint32_t ms) { sim::end_ms = ms; }
// Nút nhấn nối INPUT_PULLUP: nhấn = LOW. Danh sách (bắt đầu, độ dài) ms; dội phím 'doi_ms' ms đầu.
inline std::function<int(uint32_t)> sim_nut_nhan(std::vector<std::pair<uint32_t, uint32_t>> lan, uint32_t doi_ms = 0) {
    return [lan, doi_ms](uint32_t t) {
        for (auto [bd, dai] : lan) {
            if (t >= bd && t < bd + dai) {
                if (doi_ms && t < bd + doi_ms) return (int)((t - bd) % 2 ? HIGH : LOW);   // nảy tiếp điểm
                return (int)LOW;
            }
        }
        return (int)HIGH;
    };
}

// ===================================================================== API Arduino
inline unsigned long millis() { return sim::ms(); }
inline unsigned long micros() { return (unsigned long)sim::now_us; }
inline void delay(unsigned long ms) { sim::advance_us((uint64_t)ms * 1000); }
inline void delayMicroseconds(unsigned int us) { sim::advance_us(us); }
inline void pinMode(int p, int m) { sim::mode[p] = m; }
inline void digitalWrite(int p, int v) {
    v = v ? HIGH : LOW;
    if (!sim::out.count(p) || sim::out[p] != v) {
        sim::out[p] = v;
        if (sim::logged(p)) sim::event("%s = %s", sim::pin_name(p).c_str(), v ? "HIGH" : "LOW");
    }
}
inline int digitalRead(int p) { return sim::read_digital(p); }
inline int analogRead(int p) { auto it = sim::ain.find(p); return it != sim::ain.end() ? it->second(sim::ms()) : 0; }
inline void analogWrite(int p, int v) {
    if (v < 0) v = 0;
    if (v > 255) v = 255;
    if (!sim::pwm.count(p) || sim::pwm[p] != v) {
        sim::pwm[p] = v;
        if (sim::logged(p)) sim::event("%s PWM = %3d (%3d%%)", sim::pin_name(p).c_str(), v, v * 100 / 255);
    }
}
// ESP32 (Arduino core 3.x): PWM bằng bộ LEDC
inline std::map<int, int> ledc_bits;
inline bool ledcAttach(int p, uint32_t freq, uint8_t bits) { ledc_bits[p] = bits; (void)freq; return true; }
inline void ledcWrite(int p, uint32_t duty) {
    int maxv = (1 << ledc_bits[p]) - 1;
    if (!sim::pwm.count(p) || sim::pwm[p] != (int)duty) {
        sim::pwm[p] = duty;
        sim::event("%s LEDC duty = %u/%d (%u%%)", sim::pin_name(p).c_str(), duty, maxv, duty * 100 / maxv);
    }
}
inline unsigned long pulseIn(int p, int, unsigned long = 1000000) {
    auto it = sim::pulse.find(p);
    uint32_t us = it != sim::pulse.end() ? it->second(sim::ms()) : 0;
    sim::advance_us(us);
    return us;
}
inline std::map<int, unsigned int> tone_hz;      // chỉ ghi log khi trạng thái còi đổi
inline void tone(int p, unsigned int f, unsigned long = 0) {
    if (tone_hz[p] != f) { tone_hz[p] = f; sim::event("%s còi kêu %u Hz", sim::pin_name(p).c_str(), f); }
}
inline void noTone(int p) {
    if (tone_hz[p] != 0) { tone_hz[p] = 0; sim::event("%s còi tắt", sim::pin_name(p).c_str()); }
}
inline void attachInterrupt(int p, void (*fn)(), int mode) { sim::isrs[p] = {fn, mode, sim::read_digital(p)}; }
inline void detachInterrupt(int p) { sim::isrs.erase(p); }
inline void noInterrupts() {}
inline void interrupts() {}
template <class T> inline T constrain(T x, T a, T b) { return x < a ? a : (x > b ? b : x); }
inline long map(long x, long a, long b, long c, long d) { return (x - a) * (d - c) / (b - a) + c; }
inline uint32_t rng_state = 12345;
inline void randomSeed(unsigned long s) { rng_state = s ? s : 1; }
inline long random(long a, long b) { rng_state = rng_state * 1103515245 + 12345; return a + (long)((rng_state >> 8) % (uint32_t)(b - a)); }
inline long random(long b) { return random(0, b); }
#define IRAM_ATTR

// ===================================================================== String (rút gọn)
class String : public std::string {
public:
    String() = default;
    String(const char* s) : std::string(s) {}
    String(const std::string& s) : std::string(s) {}
    String(char c) : std::string(1, c) {}
    String(int v) : std::string(std::to_string(v)) {}
    String(long v) : std::string(std::to_string(v)) {}
    String(unsigned int v) : std::string(std::to_string(v)) {}
    String(unsigned long v) : std::string(std::to_string(v)) {}
    String(double v, int dec = 2) { char b[32]; std::snprintf(b, sizeof b, "%.*f", dec, v); assign(b); }
    int toInt() const { return std::atoi(c_str()); }
    float toFloat() const { return (float)std::atof(c_str()); }
    int indexOf(char c, int from = 0) const { auto p = find(c, from); return p == npos ? -1 : (int)p; }
    int indexOf(const char* s, int from = 0) const { auto p = find(s, from); return p == npos ? -1 : (int)p; }
    String substring(int a) const { return String(substr(a)); }
    String substring(int a, int b) const { return String(substr(a, b - a)); }
    void trim() { auto a = find_first_not_of(" \r\n\t"); auto b = find_last_not_of(" \r\n\t"); *this = a == npos ? String("") : String(substr(a, b - a + 1)); }
    void toUpperCase() { for (auto& ch : *this) ch = (char)std::toupper((unsigned char)ch); }
    bool startsWith(const char* s) const { return rfind(s, 0) == 0; }
    bool equals(const char* s) const { return *this == s; }
};
inline String operator+(const String& a, const char* b) { return String(std::string(a) + b); }
inline String operator+(const String& a, const String& b) { return String(std::string(a) + std::string(b)); }
inline String operator+(const char* a, const String& b) { return String(std::string(a) + std::string(b)); }

// ===================================================================== Serial
class SimSerial {
public:
    void begin(unsigned long) {}
    operator bool() const { return true; }
    void sim_nhap(uint32_t t_ms, const char* s) { sched_.push_back({t_ms, s}); }
    int available() { pull(); return (int)buf_.size(); }
    int read() { pull(); if (buf_.empty()) return -1; char c = buf_.front(); buf_.erase(0, 1); return (unsigned char)c; }
    String readStringUntil(char end) {
        pull();
        auto p = buf_.find(end);
        std::string s = p == std::string::npos ? buf_ : buf_.substr(0, p);
        buf_.erase(0, p == std::string::npos ? buf_.size() : p + 1);
        return String(s);
    }
    template <class T> size_t print(const T& v) { return out(fmt(v)); }
    size_t print(double v, int dec) { return out(String(v, dec)); }
    size_t print(int v, int base) { return out(base == 16 ? hex(v) : (base == 2 ? bin(v) : std::to_string(v))); }
    template <class T> size_t println(const T& v) { return out(fmt(v) + "\n"); }
    size_t println(double v, int dec) { return out(String(v, dec) + "\n"); }
    size_t println(int v, int base) { return out((base == 16 ? hex(v) : (base == 2 ? bin(v) : std::to_string(v))) + "\n"); }
    size_t println() { return out("\n"); }
    size_t printf(const char* f, ...) {
        char b[512]; va_list ap; va_start(ap, f); std::vsnprintf(b, sizeof b, f, ap); va_end(ap);
        return out(b);
    }
private:
    struct Item { uint32_t t; std::string s; };
    std::vector<Item> sched_;
    std::string buf_;
    void pull() {
        for (auto it = sched_.begin(); it != sched_.end();) {
            if (it->t <= sim::ms()) { buf_ += it->s; it = sched_.erase(it); } else ++it;
        }
    }
    static std::string fmt(const char* s) { return s; }
    static std::string fmt(const std::string& s) { return s; }
    static std::string fmt(const String& s) { return s; }
    static std::string fmt(char c) { return std::string(1, c); }
    static std::string fmt(bool b) { return b ? "1" : "0"; }
    static std::string fmt(double v) { char b[32]; std::snprintf(b, sizeof b, "%.2f", v); return b; }
    static std::string fmt(float v) { return fmt((double)v); }
    template <class T> static std::string fmt(const T& v) { return std::to_string(v); }
    static std::string hex(int v) { char b[16]; std::snprintf(b, sizeof b, "%X", v); return b; }
    static std::string bin(int v) { std::string s; do { s = char('0' + (v & 1)) + s; v >>= 1; } while (v); return s; }
    size_t out(const std::string& s) {
        std::fputs(s.c_str(), stdout);
        if (!s.empty()) sim::serial_open_line = s.back() != '\n';
        if (!sim::serial_open_line) sim::flush_pending();
        return s.size();
    }
};
inline SimSerial Serial;
