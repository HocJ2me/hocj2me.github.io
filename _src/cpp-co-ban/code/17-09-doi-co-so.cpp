// Bài 9: Đổi số thập phân sang nhị phân / thập lục phân và ngược lại (không dùng thư viện)
#include <iostream>
#include <string>

std::string sangCoSo(unsigned n, unsigned coSo) {
    const char* kyTu = "0123456789ABCDEF";
    if (n == 0) return "0";
    std::string kq;
    while (n > 0) {
        kq = kyTu[n % coSo] + kq;    // thêm chữ số vào đầu chuỗi
        n /= coSo;
    }
    return kq;
}

unsigned tuChuoi(const std::string& s, unsigned coSo) {
    unsigned kq = 0;
    for (char c : s) {
        unsigned d = (c >= '0' && c <= '9') ? c - '0' : (c & ~0x20) - 'A' + 10;   // & ~0x20: chữ thường -> hoa
        kq = kq * coSo + d;
    }
    return kq;
}

int main() {
    for (unsigned n : {10u, 255u, 2026u}) {
        std::cout << n << " = 0b" << sangCoSo(n, 2) << " = 0x" << sangCoSo(n, 16) << " = 0o" << sangCoSo(n, 8) << "\n";
    }
    std::cout << "\"1011\" (cơ số 2)  = " << tuChuoi("1011", 2) << "\n";
    std::cout << "\"7e9\"  (cơ số 16) = " << tuChuoi("7e9", 16) << "\n";
}
