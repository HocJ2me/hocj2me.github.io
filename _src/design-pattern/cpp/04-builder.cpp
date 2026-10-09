// Builder – C++17
#include <iostream>
#include <optional>
#include <string>
#include <vector>

class Robot {
public:
    class Builder;                                // khai báo trước lớp lồng

    void print() const {
        std::cout << "Robot " << name_ << " | mạch=" << board_ << " | bánh=" << wheels_
                  << " | pin=" << batteryMah_ << "mAh | BT=" << (bluetooth_ ? "có" : "không") << " | cảm biến=[";
        for (size_t i = 0; i < sensors_.size(); ++i) std::cout << (i ? ", " : "") << sensors_[i];
        std::cout << "]\n";
    }

private:
    Robot() = default;                            // chỉ Builder mới tạo được Robot
    std::string name_, board_;
    int wheels_ = 2, batteryMah_ = 1000;
    bool bluetooth_ = false;
    std::vector<std::string> sensors_;
};

class Robot::Builder {
public:
    Builder(std::string name, std::string board) {          // tham số bắt buộc
        r_.name_ = std::move(name);
        r_.board_ = std::move(board);
    }
    Builder& wheels(int n)                { r_.wheels_ = n; return *this; }
    Builder& battery(int mAh)             { r_.batteryMah_ = mAh; return *this; }
    Builder& bluetooth(bool on)           { r_.bluetooth_ = on; return *this; }
    Builder& addSensor(std::string s)     { r_.sensors_.push_back(std::move(s)); return *this; }

    // Firmware nhúng thường TẮT exceptions (-fno-exceptions) nên trả về std::optional
    // thay cho throw: rỗng nghĩa là cấu hình không hợp lệ.
    std::optional<Robot> build() const {
        if (r_.wheels_ != 2 && r_.wheels_ != 4) return std::nullopt;
        return r_;
    }
private:
    Robot r_;
};

// Director – đóng gói các "công thức" lắp ráp
class RobotDirector {
public:
    std::optional<Robot> makeLineFollower() const {
        return Robot::Builder("LINE", "Arduino Nano").addSensor("Dò line x5").battery(1200).build();
    }
    std::optional<Robot> makeSumoRobot() const {
        return Robot::Builder("SUMO", "STM32").wheels(4).addSensor("Hồng ngoại x4").battery(2200).build();
    }
};

int main() {
    auto custom = Robot::Builder("BK-01", "ESP32")
                      .wheels(4)
                      .addSensor("Siêu âm HC-SR04")
                      .addSensor("Dò line TCRT5000")
                      .battery(3000)
                      .bluetooth(true)
                      .build();
    if (custom) custom->print();

    RobotDirector director;
    director.makeLineFollower()->print();
    director.makeSumoRobot()->print();

    auto bad = Robot::Builder("LOI", "Arduino Uno").wheels(3).build();
    std::cout << "Robot 3 bánh hợp lệ? " << (bad ? "có" : "không – build() trả về rỗng") << "\n";
}
