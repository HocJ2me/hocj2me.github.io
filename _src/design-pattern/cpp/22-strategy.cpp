// Strategy – C++17. Có 3 cách cài đặt trong C++:
//  (1) interface + virtual (lúc chạy)   (2) std::function / lambda (lúc chạy)
//  (3) template (lúc BIÊN DỊCH – "policy-based design", không tốn chi phí gọi hàm ảo; rất được ưa chuộng trong nhúng)
#include <cstdio>
#include <functional>
#include <string>

// ===== (1) Strategy dạng interface =====
class PaymentStrategy {
public:
    virtual ~PaymentStrategy() = default;
    virtual const char* name() const = 0;
    virtual int fee(int amount) const = 0;
    virtual void pay(int amount) const = 0;
};

class CashPayment : public PaymentStrategy {
public:
    const char* name() const override { return "Tiền mặt"; }
    int fee(int) const override { return 0; }
    void pay(int a) const override { std::printf("   💵 Thanh toán tiền mặt khi nhận hàng: %d đ\n", a); }
};
class CardPayment : public PaymentStrategy {
public:
    explicit CardPayment(std::string n) : number_(std::move(n)) {}
    const char* name() const override { return "Thẻ"; }
    int fee(int a) const override { return a * 2 / 100; }
    void pay(int a) const override { std::printf("   💳 Trừ %d đ từ thẻ ****%s\n", a, number_.substr(number_.size() - 4).c_str()); }
private:
    std::string number_;
};
class MomoPayment : public PaymentStrategy {
public:
    explicit MomoPayment(std::string p) : phone_(std::move(p)) {}
    const char* name() const override { return "MoMo"; }
    int fee(int) const override { return 1000; }
    void pay(int a) const override { std::printf("   📱 Gửi yêu cầu %d đ tới ví MoMo %s\n", a, phone_.c_str()); }
private:
    std::string phone_;
};

// ===== Context =====
class ShoppingCart {
public:
    void addItem(const char*, int price) { subtotal_ += price; }

    void checkout(const PaymentStrategy& s) const {
        int f = s.fee(subtotal_);
        std::printf("Thanh toán bằng %s (phí %d đ)\n", s.name(), f);
        s.pay(subtotal_ + f);
    }
    // (2) strategy dạng lambda
    int total(const std::function<int(int)>& discount) const { return discount(subtotal_); }

    // (3) strategy dạng template – chọn lúc biên dịch
    template <typename DiscountPolicy>
    int totalWith() const { return DiscountPolicy::apply(subtotal_); }
private:
    int subtotal_ = 0;
};

struct StudentDiscount { static constexpr int apply(int p) { return p * 90 / 100; } };
struct NoDiscount      { static constexpr int apply(int p) { return p; } };

int main() {
    ShoppingCart cart;
    cart.addItem("Arduino Uno R3", 180000);
    cart.addItem("Bộ cảm biến 37 món", 320000);

    cart.checkout(CashPayment());
    cart.checkout(CardPayment("4111-2222-3333-4444"));
    cart.checkout(MomoPayment("0359 581 461"));

    std::printf("-- Chiến lược giảm giá dạng lambda --\n");
    auto blackFriday = [](int p) { return p > 100000 ? p - 100000 : 0; };
    std::printf("Black Friday: %d\n", cart.total(blackFriday));

    std::printf("-- Chiến lược dạng template (biên dịch) --\n");
    std::printf("Giá gốc: %d | HS-SV: %d\n", cart.totalWith<NoDiscount>(), cart.totalWith<StudentDiscount>());
}
