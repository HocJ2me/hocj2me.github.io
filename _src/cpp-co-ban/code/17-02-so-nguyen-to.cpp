// Bài 2: Kiểm tra số nguyên tố và liệt kê số nguyên tố bằng sàng Eratosthenes
#include <iostream>
#include <vector>

bool laNguyenTo(int n) {
    if (n < 2) return false;
    for (int i = 2; i * i <= n; i++)     // chỉ cần thử tới căn bậc hai của n
        if (n % i == 0) return false;
    return true;
}

std::vector<int> sang(int n) {
    std::vector<bool> laHop(n + 1, false);
    std::vector<int> kq;
    for (int i = 2; i <= n; i++) {
        if (laHop[i]) continue;
        kq.push_back(i);
        for (int j = i * i; j <= n; j += i) laHop[j] = true;   // gạch bỏ bội số
    }
    return kq;
}

int main() {
    for (int n : {1, 2, 17, 21, 97}) std::cout << n << (laNguyenTo(n) ? " là" : " không là") << " số nguyên tố\n";
    std::cout << "Các số nguyên tố <= 50: ";
    for (int p : sang(50)) std::cout << p << " ";
    std::cout << "\n";
}
