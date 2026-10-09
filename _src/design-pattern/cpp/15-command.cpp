// Command – C++17. Trong nhúng: lệnh nhận qua UART/Bluetooth được đóng gói thành
// đối tượng Command rồi đưa vào hàng đợi để vòng loop() xử lý tuần tự.
#include <iostream>
#include <memory>
#include <stack>
#include <string>

// ===== Command =====
class Command {
public:
    virtual ~Command() = default;
    virtual void execute() = 0;
    virtual void undo() = 0;
    virtual std::string name() const = 0;
};

// ===== Receivers =====
class Light {
public:
    explicit Light(std::string room) : room_(std::move(room)) {}
    void on()  { std::cout << "  💡 Bật đèn " << room_ << "\n"; }
    void off() { std::cout << "  💡 Tắt đèn " << room_ << "\n"; }
private:
    std::string room_;
};
class Fan {
public:
    int getSpeed() const { return speed_; }
    void setSpeed(int s) { speed_ = s; std::cout << "  🌀 Quạt số " << s << "\n"; }
private:
    int speed_ = 0;
};

// ===== Concrete Commands =====
class LightOnCommand : public Command {
public:
    explicit LightOnCommand(Light& l) : light_(l) {}
    void execute() override { light_.on(); }
    void undo() override    { light_.off(); }
    std::string name() const override { return "Bật đèn"; }
private:
    Light& light_;
};
class LightOffCommand : public Command {
public:
    explicit LightOffCommand(Light& l) : light_(l) {}
    void execute() override { light_.off(); }
    void undo() override    { light_.on(); }
    std::string name() const override { return "Tắt đèn"; }
private:
    Light& light_;
};
class FanSpeedCommand : public Command {
public:
    FanSpeedCommand(Fan& f, int s) : fan_(f), newSpeed_(s) {}
    void execute() override { prevSpeed_ = fan_.getSpeed(); fan_.setSpeed(newSpeed_); }
    void undo() override    { fan_.setSpeed(prevSpeed_); }
    std::string name() const override { return "Quạt số " + std::to_string(newSpeed_); }
private:
    Fan& fan_;
    int newSpeed_, prevSpeed_ = 0;            // lưu trạng thái cũ để undo
};

// ===== Invoker =====
class RemoteControl {
public:
    void press(std::unique_ptr<Command> c) {
        std::cout << "▶ " << c->name() << "\n";
        c->execute();
        history_.push(std::move(c));
    }
    void undo() {
        if (history_.empty()) { std::cout << "↩ Không còn lệnh để hoàn tác\n"; return; }
        std::cout << "↩ Hoàn tác: " << history_.top()->name() << "\n";
        history_.top()->undo();
        history_.pop();
    }
private:
    std::stack<std::unique_ptr<Command>> history_;
};

int main() {
    Light light("phòng khách");
    Fan fan;
    RemoteControl remote;

    remote.press(std::make_unique<LightOnCommand>(light));
    remote.press(std::make_unique<FanSpeedCommand>(fan, 3));
    remote.press(std::make_unique<FanSpeedCommand>(fan, 1));
    remote.press(std::make_unique<LightOffCommand>(light));

    std::cout << "--- Hoàn tác (Undo) từng bước ---\n";
    for (int i = 0; i < 5; ++i) remote.undo();
}
