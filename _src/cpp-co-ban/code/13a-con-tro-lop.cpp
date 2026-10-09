// Con trỏ lớp: con trỏ tới đối tượng, ->, this, Singleton bằng con trỏ static,
// thay đổi đối tượng đang dùng qua con trỏ (đổi chế độ lúc chạy)
#include <iostream>
#include <string>

class Robot {
public:
    explicit Robot(std::string ten) : ten_(std::move(ten)) {}
    Robot* tien(int cm) { x_ += cm; return this; }          // trả về this để gọi nối tiếp
    Robot* re(int doc)  { huong_ = (huong_ + doc) % 360; return this; }
    void baoCao() const { std::cout << "  " << ten_ << ": x = " << x_ << " cm, hướng " << huong_ << "°\n"; }
private:
    std::string ten_;
    int x_ = 0, huong_ = 0;
};

// ===== Singleton bằng con trỏ static (kiểu cổ điển) =====
class CauHinh {
public:
    static CauHinh* layThucThe() {
        if (thucThe_ == nullptr) {
            thucThe_ = new CauHinh();                         // tạo lần đầu
            std::cout << "  (tạo CauHinh)\n";
        }
        return thucThe_;
    }
    int nguongNhiet = 30;
private:
    CauHinh() = default;                                      // không cho new từ bên ngoài
    static CauHinh* thucThe_;
};
CauHinh* CauHinh::thucThe_ = nullptr;

// ===== Thay đổi đối tượng qua con trỏ: đổi "chế độ" lúc chạy =====
class CheDo {
public:
    virtual ~CheDo() = default;
    virtual void xuLy(float t) = 0;
};
class CheDoTietKiem : public CheDo {
public:
    void xuLy(float t) override { std::cout << "  [Tiết kiệm] " << t << "°C -> quạt " << (t > 32 ? "chậm" : "tắt") << "\n"; }
};
class CheDoManh : public CheDo {
public:
    void xuLy(float t) override { std::cout << "  [Mạnh] " << t << "°C -> quạt " << (t > 26 ? "MAX" : "vừa") << "\n"; }
};

int main() {
    std::cout << "== Con trỏ tới đối tượng và -> ==\n";
    Robot r("BK-01");
    Robot* p = &r;
    p->tien(20);                       // p->tien() tương đương (*p).tien()
    (*p).re(90);
    p->tien(10)->re(90)->tien(5);      // nối tiếp nhờ trả về this
    p->baoCao();

    std::cout << "\n== Mảng đối tượng & con trỏ duyệt mảng ==\n";
    Robot doi[3] = {Robot("R1"), Robot("R2"), Robot("R3")};
    for (Robot* it = doi; it != doi + 3; ++it) it->tien(10 * (it - doi + 1));
    for (const Robot& rb : doi) rb.baoCao();

    std::cout << "\n== Singleton: mọi nơi lấy về cùng một con trỏ ==\n";
    CauHinh* c1 = CauHinh::layThucThe();
    CauHinh* c2 = CauHinh::layThucThe();
    c1->nguongNhiet = 35;
    std::cout << "  c1 == c2 ? " << std::boolalpha << (c1 == c2) << ", c2->nguongNhiet = " << c2->nguongNhiet << "\n";

    std::cout << "\n== Đổi đối tượng mà con trỏ trỏ tới -> đổi hành vi lúc chạy ==\n";
    CheDoTietKiem tietKiem;
    CheDoManh manh;
    CheDo* cheDoHienTai = &tietKiem;
    for (float t : {28.0f, 33.0f}) cheDoHienTai->xuLy(t);
    std::cout << "  -- người dùng bấm nút đổi chế độ --\n";
    cheDoHienTai = &manh;                       // chỉ đổi con trỏ, không if/else
    for (float t : {28.0f, 33.0f}) cheDoHienTai->xuLy(t);
}
