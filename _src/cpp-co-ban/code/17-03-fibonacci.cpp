// Bài 3: Dãy Fibonacci – đệ quy (chậm) và vòng lặp (nhanh)
#include <cstdint>
#include <iostream>

uint64_t fibDeQuy(int n) { return n < 2 ? n : fibDeQuy(n - 1) + fibDeQuy(n - 2); }

uint64_t fibLap(int n) {
    uint64_t a = 0, b = 1;
    for (int i = 0; i < n; i++) {
        uint64_t c = a + b;
        a = b;
        b = c;
    }
    return a;
}

int main() {
    std::cout << "15 số Fibonacci đầu: ";
    for (int i = 0; i < 15; i++) std::cout << fibLap(i) << " ";
    std::cout << "\nfibDeQuy(25) = " << fibDeQuy(25) << " (gọi hàm hơn 240 000 lần)\n";
    std::cout << "fibLap(90)   = " << fibLap(90) << " (chỉ 90 vòng lặp)\n";
}
