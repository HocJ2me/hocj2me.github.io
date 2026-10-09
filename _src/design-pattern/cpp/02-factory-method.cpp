// Factory Method – C++17
#include <iostream>
#include <memory>
#include <string>
#include <typeinfo>

// ===== Product =====
class Notification {
public:
    virtual ~Notification() = default;           // destructor ảo: bắt buộc khi xoá qua con trỏ lớp cha
    virtual void send(const std::string& message) = 0;
};

// ===== Concrete Products =====
class EmailNotification : public Notification {
public:
    void send(const std::string& m) override { std::cout << "[EMAIL] " << m << "\n"; }
};

class SmsNotification : public Notification {
public:
    void send(const std::string& m) override {
        // SMS giới hạn độ dài (tính theo byte để đơn giản)
        std::cout << "[SMS]   " << (m.size() > 30 ? m.substr(0, 30) + "..." : m) << "\n";
    }
};

class ZaloNotification : public Notification {
public:
    void send(const std::string& m) override { std::cout << "[ZALO]  " << m << " 👍\n"; }
};

// ===== Creator =====
class NotificationService {
public:
    virtual ~NotificationService() = default;

    // Logic nghiệp vụ dùng sản phẩm mà KHÔNG biết lớp cụ thể của nó
    void notifyUser(const std::string& message) {
        std::unique_ptr<Notification> n = createNotification();
        std::cout << name() << " -> ";
        n->send(message);
    }

protected:
    // FACTORY METHOD – lớp con quyết định tạo đối tượng nào
    virtual std::unique_ptr<Notification> createNotification() = 0;
    virtual const char* name() const = 0;
};

// ===== Concrete Creators =====
class EmailService : public NotificationService {
protected:
    std::unique_ptr<Notification> createNotification() override { return std::make_unique<EmailNotification>(); }
    const char* name() const override { return "EmailService"; }
};

class SmsService : public NotificationService {
protected:
    std::unique_ptr<Notification> createNotification() override { return std::make_unique<SmsNotification>(); }
    const char* name() const override { return "SmsService"; }
};

class ZaloService : public NotificationService {
protected:
    std::unique_ptr<Notification> createNotification() override { return std::make_unique<ZaloNotification>(); }
    const char* name() const override { return "ZaloService"; }
};

int main() {
    EmailService email;
    SmsService sms;
    ZaloService zalo;
    NotificationService* services[] = { &email, &sms, &zalo };   // mảng tĩnh, không cấp phát
    for (NotificationService* s : services)
        s->notifyUser("Lop Design Pattern bat dau luc 19h toi nay!");
}
