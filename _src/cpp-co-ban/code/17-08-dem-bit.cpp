// Bài 8: Đếm số bit 1, kiểm tra lũy thừa của 2, đảo thứ tự bit – bài kinh điển của lập trình nhúng
#include <cstdint>
#include <iostream>

int demBit1(uint32_t x) {
    int dem = 0;
    while (x) { x &= x - 1; dem++; }        // mẹo Kernighan: mỗi vòng xoá 1 bit 1 thấp nhất
    return dem;
}

bool laLuyThua2(uint32_t x) { return x && !(x & (x - 1)); }

uint8_t daoBit(uint8_t b) {
    uint8_t kq = 0;
    for (int i = 0; i < 8; i++) {
        kq = (kq << 1) | (b & 1);
        b >>= 1;
    }
    return kq;
}

int main() {
    for (uint32_t x : {0u, 7u, 255u, 0xF0F0u, 1024u}) {
        std::cout << x << ": " << demBit1(x) << " bit 1, lũy thừa của 2? " << (laLuyThua2(x) ? "có" : "không") << "\n";
    }
    std::cout << "đảo bit 0b00000001 -> " << +daoBit(0b00000001) << " (0b10000000)\n";
    std::cout << "đảo bit 0b11010000 -> " << +daoBit(0b11010000) << " (0b00001011)\n";
    std::cout << "GCC có sẵn: __builtin_popcount(0xF0F0) = " << __builtin_popcount(0xF0F0) << "\n";
}
