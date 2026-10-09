// Bridge – C++17
#include <algorithm>
#include <iostream>
#include <string>

// ===== Implementor =====
class Device {
public:
    virtual ~Device() = default;
    virtual bool isEnabled() const = 0;
    virtual void enable() = 0;
    virtual void disable() = 0;
    virtual int getVolume() const = 0;
    virtual void setVolume(int percent) = 0;
    virtual std::string name() const = 0;
    void printStatus() const {
        std::cout << "  " << name() << ": " << (isEnabled() ? "BẬT" : "TẮT") << ", âm lượng " << getVolume() << "%\n";
    }
};

// Gom code chung của các thiết bị
class BaseDevice : public Device {
public:
    bool isEnabled() const override { return on_; }
    void enable() override  { on_ = true; }
    void disable() override { on_ = false; }
    int getVolume() const override { return volume_; }
    void setVolume(int p) override { volume_ = std::clamp(p, 0, 100); }
private:
    bool on_ = false;
    int volume_ = 30;
};

// ===== Concrete Implementors =====
class Tv : public BaseDevice    { public: std::string name() const override { return "Tv"; } };
class Radio : public BaseDevice { public: std::string name() const override { return "Radio"; } };

// ===== Abstraction – giữ tham chiếu tới Implementor: đó chính là "cây cầu" =====
class RemoteControl {
public:
    explicit RemoteControl(Device& d) : device_(d) {}
    virtual ~RemoteControl() = default;
    void togglePower() {
        if (device_.isEnabled()) device_.disable(); else device_.enable();
        std::cout << "Nút nguồn -> " << (device_.isEnabled() ? "bật" : "tắt") << "\n";
    }
    void volumeUp()   { device_.setVolume(device_.getVolume() + 10); std::cout << "Tăng âm lượng\n"; }
    void volumeDown() { device_.setVolume(device_.getVolume() - 10); std::cout << "Giảm âm lượng\n"; }
protected:
    Device& device_;
};

// ===== Refined Abstraction =====
class AdvancedRemote : public RemoteControl {
public:
    using RemoteControl::RemoteControl;           // kế thừa constructor
    void mute() { device_.setVolume(0); std::cout << "Tắt tiếng (mute)\n"; }
};

int main() {
    Tv tv;
    RemoteControl basic(tv);
    basic.togglePower();
    basic.volumeUp();
    tv.printStatus();

    std::cout << "-----\n";
    Radio radio;
    AdvancedRemote advanced(radio);
    advanced.togglePower();
    advanced.volumeUp();
    advanced.mute();
    radio.printStatus();
}
