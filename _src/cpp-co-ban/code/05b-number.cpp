// Number: thư viện toán <cmath>, ép kiểu số, số ngẫu nhiên, các hàm tiện ích hay dùng trong Arduino
#include <algorithm>
#include <cmath>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <random>

// Tự viết lại map() và constrain() của Arduino
long mapRange(long x, long inMin, long inMax, long outMin, long outMax) {
    return (x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin;
}

int main() {
    std::cout << std::fixed << std::setprecision(3);

    std::cout << "== <cmath> ==\n";
    std::cout << "  sqrt(2)      = " << std::sqrt(2.0) << "\n";
    std::cout << "  pow(2, 10)   = " << std::pow(2, 10) << "\n";
    std::cout << "  sin(30°)     = " << std::sin(30 * 3.14159265358979 / 180) << "\n";
    std::cout << "  hypot(3, 4)  = " << std::hypot(3, 4) << "   (khoảng cách)\n";
    std::cout << "  fabs(-2.5)   = " << std::fabs(-2.5) << ", abs(-7) = " << std::abs(-7) << "\n";
    std::cout << "  floor(2.7) = " << std::floor(2.7) << ", ceil(2.1) = " << std::ceil(2.1)
              << ", round(2.5) = " << std::round(2.5) << "\n";
    std::cout << "  log10(1000)  = " << std::log10(1000) << ", exp(1) = " << std::exp(1) << "\n";

    std::cout << "\n== Ép kiểu số ==\n";
    int adc = 2047;
    float volt1 = adc * 3.3 / 4095;               // 3.3 là double -> phép tính số thực
    float volt2 = adc * 33 / 40950;               // toàn số nguyên -> mất phần thập phân!
    float volt3 = static_cast<float>(adc) * 33 / 40950;
    std::cout << "  " << volt1 << " V (đúng) | " << volt2 << " V (sai: chia nguyên) | " << volt3 << " V (ép kiểu)\n";
    double d = 9.99;
    int cat = static_cast<int>(d);                // cắt phần lẻ, KHÔNG làm tròn
    int lamTron = static_cast<int>(std::lround(d));
    std::cout << "  (int)9.99 = " << cat << ", lround(9.99) = " << lamTron << "\n";

    std::cout << "\n== map() và constrain() kiểu Arduino ==\n";
    for (int bienTro : {0, 512, 1023}) {
        long pwm = mapRange(bienTro, 0, 1023, 0, 255);   // biến trở 10 bit -> PWM 8 bit
        std::cout << "  biến trở " << std::setw(4) << bienTro << " -> PWM " << pwm << "\n";
    }
    int tocDo = 300;
    std::cout << "  constrain(300, 0, 255) = " << std::clamp(tocDo, 0, 255) << "\n";

    std::cout << "\n== Số ngẫu nhiên ==\n";
    std::mt19937 gen(2026);                        // seed cố định -> lần nào chạy cũng giống nhau (dễ kiểm tra)
    std::uniform_int_distribution<int> xucXac(1, 6);
    std::cout << "  Tung xúc xắc: ";
    for (int i = 0; i < 8; i++) std::cout << xucXac(gen) << " ";
    std::cout << "\n  (Arduino: randomSeed(analogRead(A0)); random(1, 7);)\n";

    std::cout << "\n== Giới hạn & đặc biệt ==\n";
    std::cout << "  1.0 / 0 = " << 1.0 / 0 << ", sqrt(-1) = " << std::sqrt(-1.0)
              << ", isnan? " << std::boolalpha << std::isnan(std::sqrt(-1.0)) << "\n";
    float a = 0.1f + 0.2f;
    std::cout << "  So sánh số thực đúng cách: |a - 0.3| < 1e-6 ? " << (std::fabs(a - 0.3f) < 1e-6f) << "\n";
}
