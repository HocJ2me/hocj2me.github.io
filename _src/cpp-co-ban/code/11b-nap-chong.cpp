// Nạp chồng (overloading): nạp chồng hàm, constructor và toán tử
#include <cmath>
#include <iostream>
#include <string>

// ===== Nạp chồng hàm: cùng tên, khác tham số =====
void guiSerial(int v)                { std::cout << "  gửi số nguyên: " << v << "\n"; }
void guiSerial(float v)              { std::cout << "  gửi số thực: " << v << "\n"; }
void guiSerial(const std::string& s) { std::cout << "  gửi chuỗi: \"" << s << "\"\n"; }
void guiSerial(int v, int coSo)      { std::cout << "  gửi " << v << " theo cơ số " << coSo << "\n"; }

// ===== Nạp chồng toán tử: lớp Vector2 cho vị trí robot =====
class Vector2 {
public:
    Vector2(float x = 0, float y = 0) : x(x), y(y) {}           // nạp chồng constructor qua tham số mặc định

    Vector2 operator+(const Vector2& o) const { return {x + o.x, y + o.y}; }
    Vector2 operator-(const Vector2& o) const { return {x - o.x, y - o.y}; }
    Vector2 operator*(float k) const          { return {x * k, y * k}; }
    Vector2& operator+=(const Vector2& o)     { x += o.x; y += o.y; return *this; }
    bool operator==(const Vector2& o) const   { return x == o.x && y == o.y; }
    float doDai() const { return std::sqrt(x * x + y * y); }

    // operator<< để in trực tiếp bằng cout – là hàm friend (không phải thành viên)
    friend std::ostream& operator<<(std::ostream& os, const Vector2& v) {
        return os << "(" << v.x << ", " << v.y << ")";
    }

    float x, y;
};

// ===== operator[] và operator() =====
class BangLed {
public:
    bool& operator[](int i) { return led_[i]; }               // truy cập như mảng
    void operator()() const {                                   // gọi đối tượng như một hàm
        std::cout << "  ";
        for (bool b : led_) std::cout << (b ? "●" : "○");
        std::cout << "\n";
    }
private:
    bool led_[8] = {};
};

int main() {
    std::cout << "== Nạp chồng hàm ==\n";
    guiSerial(42);
    guiSerial(3.14f);
    guiSerial(std::string("OK"));
    guiSerial(255, 16);

    std::cout << "\n== Nạp chồng toán tử ==\n";
    Vector2 viTri(1, 2);
    Vector2 vanToc(0.5f, 0);
    for (int buoc = 0; buoc < 3; buoc++) viTri += vanToc;
    std::cout << "  vị trí sau 3 bước: " << viTri << "\n";
    Vector2 dich(4, 6);
    Vector2 conLai = dich - viTri;
    std::cout << "  còn cách đích: " << conLai << ", khoảng cách = " << conLai.doDai() << "\n";
    std::cout << "  vanToc * 4 = " << vanToc * 4 << ", viTri == (2.5, 2)? " << std::boolalpha
              << (viTri == Vector2(2.5f, 2)) << "\n";

    std::cout << "\n== operator[] và operator() ==\n";
    BangLed bang;
    bang[0] = bang[3] = bang[7] = true;
    bang();
}
