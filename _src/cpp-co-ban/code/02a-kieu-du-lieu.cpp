// Kiểu dữ liệu cơ bản và kiểu số nguyên cố định độ rộng (rất quan trọng trong lập trình nhúng)
#include <cstdint>
#include <iostream>
#include <limits>

int main() {
    std::cout << "== Kích thước (byte) trên máy này ==\n";
    std::cout << "bool   : " << sizeof(bool)   << "\n";
    std::cout << "char   : " << sizeof(char)   << "\n";
    std::cout << "short  : " << sizeof(short)  << "\n";
    std::cout << "int    : " << sizeof(int)    << "   (Arduino Uno: 2 byte!)\n";
    std::cout << "long   : " << sizeof(long)   << "\n";
    std::cout << "float  : " << sizeof(float)  << "\n";
    std::cout << "double : " << sizeof(double) << "   (Arduino Uno: 4 byte!)\n";

    std::cout << "\n== Kiểu cố định độ rộng <cstdint> – giống nhau trên mọi vi điều khiển ==\n";
    std::cout << "uint8_t  : 0 .. " << +std::numeric_limits<uint8_t>::max() << "\n";   // dấu + để in số, không in ký tự
    std::cout << "int8_t   : " << +std::numeric_limits<int8_t>::min() << " .. " << +std::numeric_limits<int8_t>::max() << "\n";
    std::cout << "uint16_t : 0 .. " << std::numeric_limits<uint16_t>::max() << "\n";
    std::cout << "int16_t  : " << std::numeric_limits<int16_t>::min() << " .. " << std::numeric_limits<int16_t>::max() << "\n";
    std::cout << "uint32_t : 0 .. " << std::numeric_limits<uint32_t>::max() << "\n";

    std::cout << "\n== Tràn số (overflow) ==\n";
    uint8_t dem = 255;
    dem = dem + 1;                       // 8 bit không chứa nổi 256 -> quay vòng về 0
    std::cout << "uint8_t 255 + 1 = " << +dem << "\n";
    uint16_t adc = 4095;                 // ADC 12 bit của ESP32 tối đa 4095
    std::cout << "ADC 12 bit tối đa: " << adc << " (vừa trong uint16_t)\n";

    std::cout << "\n== Số thực có sai số ==\n";
    double a = 0.1 + 0.2;
    std::cout.precision(17);
    std::cout << "0.1 + 0.2 = " << a << "\n";
    std::cout << "a == 0.3 ? " << std::boolalpha << (a == 0.3) << "  -> đừng so sánh số thực bằng ==\n";

    std::cout << "\n== Ký tự là một số ==\n";
    char c = 'A';
    std::cout << "'A' có mã ASCII " << int(c) << ", 'A' + 2 = " << char(c + 2) << "\n";
    bool denBat = true;
    std::cout << "bool true in ra: " << std::noboolalpha << denBat << "\n";
}
