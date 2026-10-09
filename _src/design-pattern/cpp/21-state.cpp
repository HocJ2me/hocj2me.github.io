// State – C++17. Máy trạng thái (FSM) là "xương sống" của firmware.
// Các đối tượng trạng thái không có dữ liệu riêng nên dùng chung bản static
// (kết hợp Singleton/Flyweight) – không cấp phát động khi chuyển trạng thái.
#include <iostream>

class VendingMachine;

// ===== State =====
class State {
public:
    virtual ~State() = default;
    virtual void insertCoin(VendingMachine& m) const = 0;
    virtual void ejectCoin(VendingMachine& m) const = 0;
    virtual void pressButton(VendingMachine& m) const = 0;
    virtual const char* name() const = 0;
};

// ===== Concrete States (khai báo) =====
class NoCoinState : public State {
public:
    void insertCoin(VendingMachine& m) const override;
    void ejectCoin(VendingMachine&) const override   { std::cout << "     Bạn chưa bỏ tiền\n"; }
    void pressButton(VendingMachine&) const override { std::cout << "     Vui lòng bỏ tiền trước\n"; }
    const char* name() const override { return "Chờ tiền"; }
    static const NoCoinState instance;
};
class HasCoinState : public State {
public:
    void insertCoin(VendingMachine&) const override  { std::cout << "     Đã có tiền rồi, không nhận thêm\n"; }
    void ejectCoin(VendingMachine& m) const override;
    void pressButton(VendingMachine& m) const override;
    const char* name() const override { return "Đã có tiền"; }
    static const HasCoinState instance;
};
class SoldOutState : public State {
public:
    void insertCoin(VendingMachine&) const override  { std::cout << "     Hết hàng! Trả lại tiền\n"; }
    void ejectCoin(VendingMachine&) const override   { std::cout << "     Không có tiền để trả\n"; }
    void pressButton(VendingMachine&) const override { std::cout << "     Hết hàng\n"; }
    const char* name() const override { return "Hết hàng"; }
    static const SoldOutState instance;
};
const NoCoinState NoCoinState::instance;
const HasCoinState HasCoinState::instance;
const SoldOutState SoldOutState::instance;

// ===== Context =====
class VendingMachine {
public:
    explicit VendingMachine(int stock)
        : state_(stock > 0 ? static_cast<const State*>(&NoCoinState::instance) : &SoldOutState::instance),
          stock_(stock) {}

    void insertCoin()  { log("Bỏ tiền");  state_->insertCoin(*this); }
    void ejectCoin()   { log("Trả tiền"); state_->ejectCoin(*this); }
    void pressButton() { log("Bấm nút");  state_->pressButton(*this); }
    void refill(int n) {
        stock_ += n;
        std::cout << "🔧 Nạp thêm " << n << " chai\n";
        setState(NoCoinState::instance);
    }

    void setState(const State& s) {
        std::cout << "     ↳ chuyển trạng thái: " << state_->name() << " → " << s.name() << "\n";
        state_ = &s;
    }
    int getStock() const { return stock_; }
    void releaseProduct() { --stock_; std::cout << "     🥤 Rơi ra 1 chai nước (còn " << stock_ << ")\n"; }

private:
    void log(const char* action) const { std::cout << "[" << state_->name() << "] " << action << "\n"; }
    const State* state_;
    int stock_;
};

// ===== Concrete States (định nghĩa – cần VendingMachine đầy đủ) =====
void NoCoinState::insertCoin(VendingMachine& m) const {
    std::cout << "     Đã nhận tiền\n";
    m.setState(HasCoinState::instance);
}
void HasCoinState::ejectCoin(VendingMachine& m) const {
    std::cout << "     Trả lại tiền\n";
    m.setState(NoCoinState::instance);
}
void HasCoinState::pressButton(VendingMachine& m) const {
    m.releaseProduct();
    if (m.getStock() > 0) m.setState(NoCoinState::instance);
    else                  m.setState(SoldOutState::instance);
}

int main() {
    VendingMachine vm(2);
    vm.pressButton();
    vm.insertCoin();
    vm.insertCoin();
    vm.pressButton();

    vm.insertCoin();
    vm.ejectCoin();

    vm.insertCoin();
    vm.pressButton();
    vm.insertCoin();
    vm.refill(5);
    vm.insertCoin();
}
