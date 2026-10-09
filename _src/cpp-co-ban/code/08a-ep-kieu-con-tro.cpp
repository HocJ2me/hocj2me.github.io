// Ép kiểu con trỏ: xem một số nguyên như dãy byte, int <-> char, endian, đóng gói gói tin, thanh ghi
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <iostream>

void inByte(const char* ten, const void* p, size_t n) {
    const uint8_t* b = static_cast<const uint8_t*>(p);   // void* -> uint8_t* để đọc từng byte
    std::printf("  %-12s:", ten);
    for (size_t i = 0; i < n; i++) std::printf(" %02X", b[i]);
    std::printf("\n");
}

// Mô phỏng một khối thanh ghi ngoại vi (thực tế nằm ở địa chỉ cố định, vd 0x40020000 trên STM32)
struct GPIO_TypeDef {
    volatile uint32_t MODER;
    volatile uint32_t ODR;
};
uint32_t vungNhoGiaLap[2] = {0, 0};

int main() {
    std::cout << "== int <-> char ==\n";
    char c = 'B';
    int maAscii = c;                                    // char -> int: lấy mã
    char chuSo = '0' + 7;                               // int -> ký tự chữ số
    int giaTri = '9' - '0';                             // ký tự chữ số -> int
    std::cout << "  'B' = " << maAscii << ", '0'+7 = '" << chuSo << "', '9'-'0' = " << giaTri << "\n";
    int lon = 300;
    char cat = static_cast<char>(lon);                  // chỉ giữ 8 bit thấp: 300 = 0x12C -> 0x2C
    std::cout << "  (char)300 = " << int(static_cast<unsigned char>(cat)) << " (mất dữ liệu!)\n";

    std::cout << "\n== Xem số nguyên 32 bit như 4 byte (ép uint32_t* -> uint8_t*) ==\n";
    uint32_t so = 0x12345678;
    uint8_t* pb = reinterpret_cast<uint8_t*>(&so);
    std::printf("  pb[0..3] = %02X %02X %02X %02X\n", pb[0], pb[1], pb[2], pb[3]);
    std::cout << "  -> " << (pb[0] == 0x78 ? "LITTLE endian (x86, ARM, ESP32: byte thấp nằm trước)" : "BIG endian") << "\n";

    std::cout << "\n== Đóng gói dữ liệu cảm biến thành mảng byte để gửi UART/LoRa ==\n";
    #pragma pack(push, 1)                               // bỏ byte đệm giữa các trường
    struct GoiTin {
        uint8_t  id;
        int16_t  nhietDoX10;                            // 28.5°C gửi dưới dạng 285
        uint16_t doAm;
        float    apSuat;
    };
    #pragma pack(pop)
    GoiTin g{0x01, 285, 65, 1013.25f};
    inByte("GoiTin", &g, sizeof(g));
    std::cout << "  sizeof(GoiTin) = " << sizeof(g) << " byte (không pack sẽ là 12)\n";
    // Phía nhận: chép mảng byte trở lại struct bằng memcpy (an toàn hơn ép con trỏ)
    uint8_t nhan[sizeof(GoiTin)];
    std::memcpy(nhan, &g, sizeof(g));
    GoiTin g2;
    std::memcpy(&g2, nhan, sizeof(g2));
    std::cout << "  Phía nhận: id=" << +g2.id << ", T=" << g2.nhietDoX10 / 10.0 << "°C, H=" << g2.doAm
              << "%, P=" << g2.apSuat << " hPa\n";

    std::cout << "\n== Lấy bit pattern của float ==\n";
    float f = 1.0f;
    uint32_t bits;
    std::memcpy(&bits, &f, sizeof(bits));               // cách đúng chuẩn (tránh vi phạm strict aliasing)
    std::printf("  1.0f = 0x%08X (dấu | mũ | phần định trị theo IEEE-754)\n", bits);

    std::cout << "\n== Ép địa chỉ thành con trỏ tới thanh ghi (cách viết driver) ==\n";
    // Trên STM32: #define GPIOA ((GPIO_TypeDef*)0x40020000)
    GPIO_TypeDef* GPIOA = reinterpret_cast<GPIO_TypeDef*>(vungNhoGiaLap);
    GPIOA->MODER |= (1u << (5 * 2));                    // chân 5 = output
    GPIOA->ODR   |= (1u << 5);                          // xuất mức 1 ra chân 5
    std::printf("  MODER = 0x%08X, ODR = 0x%08X\n", (unsigned)GPIOA->MODER, (unsigned)GPIOA->ODR);

    std::cout << "\n== Các toán tử ép kiểu của C++ ==\n";
    std::cout << "  static_cast       : chuyển đổi hợp lệ (số <-> số, void* -> T*)\n";
    std::cout << "  reinterpret_cast  : diễn giải lại bit/địa chỉ (thanh ghi, byte) – nguy hiểm\n";
    std::cout << "  const_cast        : bỏ const – hầu như không nên dùng\n";
    std::cout << "  dynamic_cast      : ép xuống lớp con có kiểm tra (cần RTTI)\n";
}
