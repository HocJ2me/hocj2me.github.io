// Con trỏ hàm: callback, bảng xử lý lệnh, so sánh với std::function và lambda
#include <cstdlib>
#include <cstring>
#include <functional>
#include <iostream>

int cong(int a, int b) { return a + b; }
int nhan(int a, int b) { return a * b; }

// Hàm nhận một hàm khác làm tham số (callback)
int apDung(int (*phepToan)(int, int), int a, int b) { return phepToan(a, b); }

// Kiểu con trỏ hàm có tên cho dễ đọc
using HamXuLy = void (*)(int);

void batLed(int v)    { std::cout << "  -> LED " << (v ? "bật" : "tắt") << "\n"; }
void quayServo(int v) { std::cout << "  -> Servo quay " << v << " độ\n"; }
void datToc(int v)    { std::cout << "  -> Động cơ tốc độ " << v << "\n"; }

// Bảng tra lệnh: tên -> hàm xử lý. Thêm lệnh mới chỉ cần thêm một dòng.
struct MucLenh { const char* ten; HamXuLy ham; };
const MucLenh BANG_LENH[] = {
    {"LED",   batLed},
    {"SERVO", quayServo},
    {"SPEED", datToc},
};

void thucThi(const char* ten, int giaTri) {
    for (const MucLenh& m : BANG_LENH) {
        if (std::strcmp(m.ten, ten) == 0) { m.ham(giaTri); return; }
    }
    std::cout << "  -> Không có lệnh " << ten << "\n";
}

// Giả lập attachInterrupt(pin, callback): đăng ký hàm sẽ được gọi khi có sự kiện
void (*callbackNut)() = nullptr;
void attachInterrupt(void (*cb)()) { callbackNut = cb; }
void khiNhanNut() { std::cout << "  [ISR] Nút được nhấn!\n"; }

int soSanhTang(const void* a, const void* b) {
    return *static_cast<const int*>(a) - *static_cast<const int*>(b);
}

int main() {
    std::cout << "== Con trỏ hàm cơ bản ==\n";
    int (*f)(int, int) = cong;
    std::cout << "  f = cong: f(3, 4) = " << f(3, 4) << "\n";
    f = nhan;
    std::cout << "  f = nhan: f(3, 4) = " << f(3, 4) << "\n";
    std::cout << "  apDung(cong, 10, 5) = " << apDung(cong, 10, 5) << "\n";

    std::cout << "\n== Bảng xử lý lệnh ==\n";
    thucThi("LED", 1);
    thucThi("SERVO", 90);
    thucThi("BUZZER", 1);

    std::cout << "\n== Callback kiểu attachInterrupt ==\n";
    attachInterrupt(khiNhanNut);
    if (callbackNut) callbackNut();          // phần cứng "gọi lại" khi có ngắt

    std::cout << "\n== qsort của C nhận con trỏ hàm so sánh ==\n  ";
    int a[] = {42, 7, 19, 3, 25};
    std::qsort(a, 5, sizeof(int), soSanhTang);
    for (int v : a) std::cout << v << " ";
    std::cout << "\n";

    std::cout << "\n== std::function + lambda: linh hoạt hơn (có thể mang theo biến) ==\n";
    int nguong = 30;
    std::function<bool(int)> kiemTra = [nguong](int t) { return t > nguong; };   // lambda "bắt" biến nguong
    for (int t : {25, 35}) std::cout << "  " << t << "°C vượt ngưỡng? " << std::boolalpha << kiemTra(t) << "\n";
    std::cout << "  sizeof(con trỏ hàm) = " << sizeof(f) << ", sizeof(std::function) = " << sizeof(kiemTra)
              << " -> trên MCU ưu tiên con trỏ hàm\n";
}
