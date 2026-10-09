// Bộ nhớ động: stack vs heap, new/delete, rò rỉ bộ nhớ, con trỏ thông minh, placement new vào bộ đệm tĩnh
#include <iostream>
#include <memory>
#include <new>

class GoiTin {
public:
    explicit GoiTin(int id) : id_(id) { soDangSong++; std::cout << "    + GoiTin " << id_ << "\n"; }
    ~GoiTin() { soDangSong--; std::cout << "    - GoiTin " << id_ << "\n"; }
    int id() const { return id_; }
    static int soDangSong;
private:
    int id_;
    char payload_[60] = {};
};
int GoiTin::soDangSong = 0;

int main() {
    std::cout << "== Stack: biến cục bộ tự giải phóng ==\n";
    {
        GoiTin g(1);
    }

    std::cout << "\n== Heap với new / delete ==\n";
    GoiTin* p = new GoiTin(2);              // cấp phát trên heap, sống tới khi delete
    std::cout << "    dùng p->id() = " << p->id() << "\n";
    delete p;                               // QUÊN dòng này = rò rỉ bộ nhớ
    p = nullptr;                            // tránh con trỏ treo (dangling)

    std::cout << "\n== Mảng động new[] / delete[] ==\n";
    int n = 5;                              // kích thước chỉ biết lúc chạy
    int* mau = new int[n];
    for (int i = 0; i < n; i++) mau[i] = i * i;
    std::cout << "    mau[4] = " << mau[4] << "\n";
    delete[] mau;                           // mảng phải dùng delete[]

    std::cout << "\n== Rò rỉ bộ nhớ (memory leak) ==\n";
    for (int i = 0; i < 3; i++) {
        GoiTin* ro = new GoiTin(10 + i);    // cố ý không delete
        (void)ro;
    }
    std::cout << "    Còn " << GoiTin::soDangSong << " gói tin không ai giải phóng! (trên MCU sẽ cạn RAM dần rồi treo)\n";

    std::cout << "\n== unique_ptr: một chủ sở hữu, tự delete ==\n";
    {
        std::unique_ptr<GoiTin> u = std::make_unique<GoiTin>(20);
        std::unique_ptr<GoiTin> u2 = std::move(u);      // chuyển quyền sở hữu, không sao chép được
        std::cout << "    u rỗng? " << std::boolalpha << (u == nullptr) << ", u2->id() = " << u2->id() << "\n";
    }

    std::cout << "\n== shared_ptr: nhiều chủ sở hữu, đếm tham chiếu ==\n";
    {
        auto s1 = std::make_shared<GoiTin>(30);
        {
            auto s2 = s1;
            std::cout << "    use_count = " << s1.use_count() << "\n";
        }
        std::cout << "    use_count = " << s1.use_count() << "\n";
    }

    std::cout << "\n== Placement new: dựng đối tượng trong bộ đệm TĨNH (không đụng heap) ==\n";
    alignas(GoiTin) static unsigned char vungNho[sizeof(GoiTin)];
    GoiTin* g = new (vungNho) GoiTin(40);
    std::cout << "    đối tượng nằm trong vungNho? " << (static_cast<void*>(g) == vungNho) << "\n";
    g->~GoiTin();                           // tự gọi destructor, KHÔNG delete

    std::cout << "\n  sizeof(GoiTin) = " << sizeof(GoiTin) << " byte. Arduino Uno chỉ có 2048 byte RAM!\n";
    std::cout << "  Còn sống ở cuối chương trình: " << GoiTin::soDangSong << " (chính là 3 gói bị rò rỉ)\n";
}
