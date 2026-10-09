// Adapter – C++17. Tình huống nhúng điển hình: driver cảm biến từ thư viện khác
// có API không khớp với lớp trừu tượng (HAL) mà firmware của ta đang dùng.
#include <cstdio>
#include <string>

// ===== Target – interface mà firmware mong đợi =====
class TemperatureSensor {
public:
    virtual ~TemperatureSensor() = default;
    virtual std::string name() const = 0;
    virtual float readCelsius() = 0;
};

// Client
class Dashboard {
public:
    void show(TemperatureSensor& s) {
        float c = s.readCelsius();
        std::printf("%5.1f°C %s  <- %s\n", c, c > 30 ? "🔥 Nóng" : "🙂 Ổn  ", s.name().c_str());
    }
};

// Lớp đã tương thích sẵn
class Dht11Sensor : public TemperatureSensor {
public:
    std::string name() const override { return "DHT11 (nội địa)"; }
    float readCelsius() override { return 28.5f; }
};

// ===== Adaptee – thư viện bên thứ ba, KHÔNG được sửa =====
class UsFahrenheitSensor {
public:
    explicit UsFahrenheitSensor(const char* serial) : serial_(serial) {}
    const char* getSerialNumber() const { return serial_; }
    float getTempF() const { return 95.0f; }          // 95°F = 35°C
private:
    const char* serial_;
};

// ===== Cách 1 – Object Adapter (composition): giữ THAM CHIẾU tới adaptee =====
class FahrenheitSensorAdapter : public TemperatureSensor {
public:
    explicit FahrenheitSensorAdapter(UsFahrenheitSensor& adaptee) : adaptee_(adaptee) {}
    std::string name() const override { return std::string("Adapter[") + adaptee_.getSerialNumber() + "]"; }
    float readCelsius() override { return (adaptee_.getTempF() - 32.0f) * 5.0f / 9.0f; }
private:
    UsFahrenheitSensor& adaptee_;
};

// ===== Cách 2 – Class Adapter: đa kế thừa (C++ hỗ trợ) =====
// public kế thừa Target, private kế thừa Adaptee (chỉ dùng cài đặt, không lộ API cũ ra ngoài)
class FahrenheitClassAdapter : public TemperatureSensor, private UsFahrenheitSensor {
public:
    explicit FahrenheitClassAdapter(const char* serial) : UsFahrenheitSensor(serial) {}
    std::string name() const override { return std::string("ClassAdapter[") + getSerialNumber() + "]"; }
    float readCelsius() override { return (getTempF() - 32.0f) * 5.0f / 9.0f; }
};

int main() {
    Dht11Sensor dht;
    UsFahrenheitSensor usSensor("US-77");
    FahrenheitSensorAdapter adapter(usSensor);
    FahrenheitClassAdapter classAdapter("US-99");

    TemperatureSensor* sensors[] = { &dht, &adapter, &classAdapter };
    Dashboard dashboard;
    for (TemperatureSensor* s : sensors) dashboard.show(*s);
}
