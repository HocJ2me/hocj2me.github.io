// Template: hàm mẫu, lớp mẫu, tham số không phải kiểu (kích thước), chuyên biệt hoá
#include <cstdint>
#include <iostream>
#include <string>

// ===== Hàm mẫu: viết một lần, dùng cho nhiều kiểu =====
template <typename T>
T lonNhat(T a, T b) { return a > b ? a : b; }

template <typename T>
T gioiHan(T x, T thap, T cao) { return x < thap ? thap : (x > cao ? cao : x); }

// ===== Lớp mẫu: bộ đệm vòng kích thước cố định – KHÔNG dùng heap, rất hợp vi điều khiển =====
template <typename T, size_t N>
class RingBuffer {
public:
    bool push(const T& v) {
        if (dem_ == N) return false;              // đầy
        buf_[duoi_] = v;
        duoi_ = (duoi_ + 1) % N;
        dem_++;
        return true;
    }
    bool pop(T& ra) {
        if (dem_ == 0) return false;              // rỗng
        ra = buf_[dau_];
        dau_ = (dau_ + 1) % N;
        dem_--;
        return true;
    }
    size_t size() const { return dem_; }
    static constexpr size_t capacity() { return N; }
private:
    T buf_[N];
    size_t dau_ = 0, duoi_ = 0, dem_ = 0;
};

// ===== Chuyên biệt hoá: xử lý riêng cho một kiểu =====
template <typename T>
std::string moTa(const T& v) { return "giá trị " + std::to_string(v); }
template <>
std::string moTa<bool>(const bool& v) { return v ? "BẬT" : "TẮT"; }

int main() {
    std::cout << "== Hàm mẫu ==\n";
    std::cout << "  lonNhat(3, 7) = " << lonNhat(3, 7) << "\n";
    std::cout << "  lonNhat(2.5, 1.5) = " << lonNhat(2.5, 1.5) << "\n";
    std::cout << "  lonNhat<std::string>(\"abc\", \"abd\") = " << lonNhat<std::string>("abc", "abd") << "\n";
    std::cout << "  gioiHan(300, 0, 255) = " << gioiHan(300, 0, 255) << "\n";

    std::cout << "\n== Lớp mẫu RingBuffer<uint16_t, 4> ==\n";
    RingBuffer<uint16_t, 4> hangDoiAdc;
    for (uint16_t v : {100, 200, 300, 400, 500}) {
        bool ok = hangDoiAdc.push(v);
        std::cout << "  push " << v << (ok ? " ok" : " -> ĐẦY, bỏ qua") << "\n";
    }
    uint16_t v;
    while (hangDoiAdc.pop(v)) std::cout << "  pop " << v << "\n";
    std::cout << "  sizeof(RingBuffer<uint16_t,4>) = " << sizeof(hangDoiAdc) << " byte, cố định lúc biên dịch\n";

    RingBuffer<std::string, 2> lenh;
    lenh.push("LED:1");
    std::string s;
    lenh.pop(s);
    std::cout << "  RingBuffer<std::string, 2> dùng cho lệnh: " << s << "\n";

    std::cout << "\n== Chuyên biệt hoá ==\n";
    std::cout << "  moTa(42) = " << moTa(42) << ", moTa(true) = " << moTa(true) << "\n";
}
