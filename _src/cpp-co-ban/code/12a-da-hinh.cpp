// Tính đa hình (polymorphism): hàm ảo (virtual), override, liên kết động, destructor ảo
#include <iostream>
#include <memory>

class DongCo {
public:
    virtual ~DongCo() { std::cout << "    ~DongCo()\n"; }     // destructor ẢO – bắt buộc với lớp cha đa hình
    virtual void chay(int tocDo) { std::cout << "  DongCo chung chạy " << tocDo << "\n"; }
    void tenLop() { std::cout << "  (hàm KHÔNG ảo của DongCo)\n"; }
};

class DongCoDC : public DongCo {
public:
    ~DongCoDC() override { std::cout << "    ~DongCoDC() – tắt PWM\n"; }
    void chay(int tocDo) override { std::cout << "  Động cơ DC: PWM duty = " << tocDo * 100 / 255 << "%\n"; }
    void tenLop() { std::cout << "  (hàm KHÔNG ảo của DongCoDC)\n"; }
};

class DongCoBuoc : public DongCo {
public:
    ~DongCoBuoc() override { std::cout << "    ~DongCoBuoc() – nhả cuộn dây\n"; }
    void chay(int tocDo) override { std::cout << "  Động cơ bước: " << tocDo * 10 << " bước/giây\n"; }
};

class Servo : public DongCo {
public:
    void chay(int goc) override { std::cout << "  Servo quay tới " << goc * 180 / 255 << " độ\n"; }
};

// Hàm này viết MỘT LẦN, chạy đúng với MỌI loại động cơ – đó là đa hình
void khoiDong(DongCo& dc, int tocDo) { dc.chay(tocDo); }

int main() {
    std::cout << "== Liên kết động: hàm nào được gọi do KIỂU THẬT của đối tượng quyết định ==\n";
    DongCoDC dc;
    DongCoBuoc buoc;
    Servo servo;
    DongCo* ds[] = {&dc, &buoc, &servo};
    for (DongCo* p : ds) p->chay(128);

    std::cout << "\n== Qua tham chiếu cũng vậy ==\n";
    khoiDong(buoc, 200);

    std::cout << "\n== Hàm KHÔNG ảo: gọi theo KIỂU CON TRỎ (liên kết tĩnh) ==\n";
    DongCo* p = &dc;
    p->tenLop();      // gọi bản của DongCo dù đối tượng là DongCoDC
    dc.tenLop();

    std::cout << "\n== Destructor ảo: xoá qua con trỏ lớp cha vẫn gọi đủ destructor lớp con ==\n";
    {
        std::unique_ptr<DongCo> dongCo = std::make_unique<DongCoDC>();
        dongCo->chay(255);
    }

    std::cout << "\n== Chi phí của đa hình ==\n";
    struct KhongAo { int x; };
    struct CoAo { virtual ~CoAo() = default; int x; };
    std::cout << "  sizeof(lớp không ảo) = " << sizeof(KhongAo) << ", sizeof(lớp có hàm ảo) = " << sizeof(CoAo)
              << " (thêm con trỏ vtable)\n";
    std::cout << "\n== Hết main ==\n";
}
