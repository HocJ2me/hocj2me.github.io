// Mediator – C++17
#include <iostream>
#include <string>
#include <vector>

class User;

// ===== Mediator =====
class ChatRoom {
public:
    virtual ~ChatRoom() = default;
    virtual void join(User& u) = 0;
    virtual void broadcast(const std::string& msg, const User& from) = 0;
    virtual void sendPrivate(const std::string& msg, const User& from, const std::string& to) = 0;
};

// ===== Colleague =====
class User {
public:
    User(std::string name, ChatRoom& room) : name_(std::move(name)), room_(room) { room_.join(*this); }
    virtual ~User() = default;
    const std::string& getName() const { return name_; }
    virtual bool isTeacher() const { return false; }

    void send(const std::string& msg) {
        std::cout << name_ << " gửi: " << msg << "\n";
        room_.broadcast(msg, *this);
    }
    void sendPrivate(const std::string& to, const std::string& msg) {
        std::cout << name_ << " nhắn riêng " << to << ": " << msg << "\n";
        room_.sendPrivate(msg, *this, to);
    }
    void receive(const std::string& msg, const std::string& from) const {
        std::cout << "    -> " << name_ << " nhận từ " << from << ": " << msg << "\n";
    }
protected:
    std::string name_;
    ChatRoom& room_;                       // chỉ biết mediator, không biết User khác
};

class Student : public User { public: using User::User; };
class Teacher : public User { public: using User::User; bool isTeacher() const override { return true; } };

// ===== Concrete Mediator =====
class ClassChatRoom : public ChatRoom {
public:
    explicit ClassChatRoom(std::string name) : name_(std::move(name)) {}
    void join(User& u) override {
        users_.push_back(&u);
        std::cout << "[" << name_ << "] " << u.getName() << " đã tham gia\n";
    }
    void broadcast(const std::string& msg, const User& from) override {
        std::string tag = from.isTeacher() ? "📌 " : "";           // quy tắc nằm ở mediator
        for (User* u : users_)
            if (u != &from) u->receive(tag + msg, from.getName());
    }
    void sendPrivate(const std::string& msg, const User& from, const std::string& to) override {
        for (User* u : users_)
            if (u->getName() == to) { u->receive("(riêng) " + msg, from.getName()); return; }
    }
private:
    std::string name_;
    std::vector<User*> users_;
};

int main() {
    ClassChatRoom room("Lớp 10A1");
    Teacher teacher("Thầy Tuyền", room);
    Student an("An", room), binh("Bình", room), chi("Chi", room);

    an.send("Mọi người làm bài tập Builder chưa?");
    teacher.send("Hạn nộp là 20h tối nay nhé!");
    binh.sendPrivate("Chi", "Cho mình mượn vở ghi với");
    chi.send("Bài này dài quá :(");
}
