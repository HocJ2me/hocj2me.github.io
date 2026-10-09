// Toán tử: số học, so sánh, logic, gán, bit (thao tác thanh ghi), ba ngôi
#include <bitset>
#include <cstdint>
#include <iostream>

void inBit(const char* ten, uint8_t v) {
    std::cout << "  " << ten << " = 0b" << std::bitset<8>(v) << " (" << +v << ")\n";
}

int main() {
    std::cout << "== Số học ==\n";
    int a = 17, b = 5;
    std::cout << "  17 + 5 = " << a + b << ", 17 - 5 = " << a - b << ", 17 * 5 = " << a * b << "\n";
    std::cout << "  17 / 5 = " << a / b << "   (chia SỐ NGUYÊN bỏ phần lẻ!)\n";
    std::cout << "  17 % 5 = " << a % b << "   (chia lấy dư)\n";
    std::cout << "  17.0 / 5 = " << 17.0 / b << "\n";
    int i = 5;
    int x = i++;      // dùng giá trị cũ rồi mới tăng
    int y = ++i;      // tăng trước rồi mới dùng
    std::cout << "  x = i++ -> " << x << ", y = ++i -> " << y << ", i = " << i << "\n";

    std::cout << "\n== So sánh & logic ==\n";
    float nhietDo = 31.5f;
    bool troiNong = nhietDo > 30;
    bool coNguoi = true;
    std::cout << std::boolalpha;
    std::cout << "  troiNong && coNguoi = " << (troiNong && coNguoi) << "\n";
    std::cout << "  troiNong || false   = " << (troiNong || false) << "\n";
    std::cout << "  !troiNong           = " << !troiNong << "\n";
    // Short-circuit: vế phải KHÔNG được tính nếu vế trái đã quyết định kết quả
    int* p = nullptr;
    if (p != nullptr && *p > 0) std::cout << "không bao giờ tới đây\n";
    std::cout << "  p != nullptr && *p > 0 -> an toàn nhờ short-circuit\n";

    std::cout << "\n== Toán tử gán kết hợp ==\n";
    int tong = 10;
    tong += 5; tong *= 2; tong -= 4; tong /= 2;
    std::cout << "  ((10 + 5) * 2 - 4) / 2 = " << tong << "\n";

    std::cout << "\n== Toán tử BIT – thao tác thanh ghi trong vi điều khiển ==\n";
    uint8_t PORTB = 0b00000000;            // giả lập thanh ghi 8 bit điều khiển 8 chân
    PORTB |= (1 << 5);                     // ĐẶT bit 5 = 1 (bật LED chân 13 Arduino Uno)
    inBit("Đặt bit 5   ", PORTB);
    PORTB |= (1 << 0) | (1 << 2);          // đặt nhiều bit cùng lúc
    inBit("Đặt bit 0,2 ", PORTB);
    PORTB &= ~(1 << 0);                    // XOÁ bit 0
    inBit("Xoá bit 0   ", PORTB);
    PORTB ^= (1 << 5);                     // ĐẢO bit 5 (nhấp nháy LED)
    inBit("Đảo bit 5   ", PORTB);
    bool bit2 = PORTB & (1 << 2);          // ĐỌC bit 2
    std::cout << "  Bit 2 đang = " << bit2 << "\n";
    uint16_t giaTri = 0xABCD;
    uint8_t byteCao = giaTri >> 8;         // lấy byte cao
    uint8_t byteThap = giaTri & 0xFF;      // lấy byte thấp
    std::cout << std::hex << std::uppercase;
    std::cout << "  0xABCD -> byte cao 0x" << +byteCao << ", byte thấp 0x" << +byteThap << "\n";
    std::cout << std::dec;
    std::cout << "  1 << 4 = " << (1 << 4) << " (nhân 2^4),  160 >> 3 = " << (160 >> 3) << " (chia 2^3)\n";

    std::cout << "\n== Ba ngôi & thứ tự ưu tiên ==\n";
    int pin = 87;
    std::cout << "  Pin " << pin << "%: " << (pin < 20 ? "SẮP HẾT" : "ổn") << "\n";
    std::cout << "  2 + 3 * 4 = " << 2 + 3 * 4 << ", (2 + 3) * 4 = " << (2 + 3) * 4 << "\n";
    uint8_t reg = 0b0100;
    // Bẫy: == ưu tiên cao hơn & -> phải có ngoặc
    std::cout << "  (reg & 4) == 4 -> " << ((reg & 4) == 4) << "\n";
}
