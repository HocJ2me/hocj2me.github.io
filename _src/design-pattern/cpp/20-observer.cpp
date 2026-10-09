// Observer – C++17. Rất hợp với firmware IoT: một cảm biến, nhiều nơi cần dữ liệu
// (màn hình, relay, gửi MQTT). Danh sách observer dùng mảng tĩnh – không cấp phát động.
#include <array>
#include <iostream>
#include <string>

// ===== Observer =====
class Observer {
public:
    virtual ~Observer() = default;
    virtual void update(float temperature, float humidity) = 0;
};

// ===== Subject =====
class Subject {
public:
    virtual ~Subject() = default;
    virtual bool subscribe(Observer& o) = 0;
    virtual void unsubscribe(Observer& o) = 0;
    virtual void notifyObservers() = 0;
};

// ===== ConcreteSubject =====
class WeatherStation : public Subject {
public:
    static constexpr size_t MAX_OBSERVERS = 8;

    bool subscribe(Observer& o) override {
        for (auto& slot : observers_) if (!slot) { slot = &o; return true; }
        return false;                                          // hết chỗ
    }
    void unsubscribe(Observer& o) override {
        for (auto& slot : observers_) if (slot == &o) slot = nullptr;
    }
    void notifyObservers() override {
        for (Observer* o : observers_) if (o) o->update(temperature_, humidity_);
    }
    void setMeasurements(float t, float h) {                  // gọi từ loop() sau khi đọc cảm biến
        std::cout << "📡 Trạm đo: " << t << "°C, " << h << "%\n";
        temperature_ = t; humidity_ = h;
        notifyObservers();
    }
private:
    std::array<Observer*, MAX_OBSERVERS> observers_{};       // toàn nullptr lúc đầu
    float temperature_ = 0, humidity_ = 0;
};

// ===== ConcreteObservers =====
class LcdDisplay : public Observer {
public:
    void update(float t, float h) override { std::cout << "   🖥️  LCD: " << t << "°C | " << h << "%\n"; }
};
class AutoFan : public Observer {                             // điều khiển relay quạt
public:
    explicit AutoFan(float threshold) : threshold_(threshold) {}
    void update(float t, float) override {
        std::cout << "   🌀 Quạt: " << (t > threshold_ ? "BẬT (relay HIGH)" : "tắt") << "\n";
    }
private:
    float threshold_;
};
class PhoneApp : public Observer {                            // gửi MQTT lên điện thoại
public:
    explicit PhoneApp(std::string owner) : owner_(std::move(owner)) {}
    void update(float t, float) override { std::cout << "   📱 MQTT tới " << owner_ << ": nhiệt độ " << t << "°C\n"; }
private:
    std::string owner_;
};

int main() {
    WeatherStation station;
    LcdDisplay lcd;
    AutoFan fan(30);
    PhoneApp app("An");

    station.subscribe(lcd);
    station.subscribe(fan);
    station.subscribe(app);

    station.setMeasurements(27.5f, 70);
    station.setMeasurements(32.0f, 55);

    std::cout << "-- App của An huỷ đăng ký --\n";
    station.unsubscribe(app);
    station.setMeasurements(29.0f, 60);
}
