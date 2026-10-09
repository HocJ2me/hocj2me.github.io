// Bài 7: Ước chung lớn nhất (thuật toán Euclid) và bội chung nhỏ nhất – rút gọn phân số
#include <iostream>

int ucln(int a, int b) {
    while (b != 0) { int r = a % b; a = b; b = r; }
    return a;
}

long bcnn(int a, int b) { return (long)a / ucln(a, b) * b;   // chia trước để tránh tràn số
}

int main() {
    std::cout << "UCLN(48, 18) = " << ucln(48, 18) << ", BCNN(48, 18) = " << bcnn(48, 18) << "\n";
    std::cout << "UCLN(17, 5)  = " << ucln(17, 5) << " (nguyên tố cùng nhau)\n";
    int tu = 84, mau = 126;
    int g = ucln(tu, mau);
    std::cout << "Rút gọn " << tu << "/" << mau << " = " << tu / g << "/" << mau / g << "\n";
    // Ứng dụng: hai đèn nháy chu kỳ 400ms và 600ms sẽ cùng sáng lại sau BCNN ms
    std::cout << "Đèn 400ms và đèn 600ms cùng nháy lại sau " << bcnn(400, 600) << " ms\n";
}
