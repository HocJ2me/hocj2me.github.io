// Bài 1: Tính tổng các chữ số và đảo ngược một số nguyên
#include <iostream>

int tongChuSo(long n) {
    if (n < 0) n = -n;
    int tong = 0;
    while (n > 0) {
        tong += n % 10;   // lấy chữ số cuối
        n /= 10;          // bỏ chữ số cuối
    }
    return tong;
}

long daoNguoc(long n) {
    long kq = 0;
    while (n != 0) {
        kq = kq * 10 + n % 10;
        n /= 10;
    }
    return kq;
}

int main() {
    for (long n : {12345L, 9081L, 7L, 1000L}) {
        std::cout << n << ": tổng chữ số = " << tongChuSo(n) << ", đảo ngược = " << daoNguoc(n) << "\n";
    }
}
