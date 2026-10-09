// Câu lệnh rẽ nhánh: if, else if, else, switch
#include <iostream>

void xuLyNhietDo(float t) {
    std::cout << "  " << t << "°C -> ";
    if (t < 18) {
        std::cout << "lạnh: bật máy sưởi\n";
    } else if (t <= 28) {
        std::cout << "dễ chịu: tắt hết\n";
    } else if (t <= 35) {
        std::cout << "nóng: bật quạt\n";
    } else {
        std::cout << "quá nóng: bật quạt + còi cảnh báo\n";
    }
}

// Lệnh nhận qua Serial thường là 1 ký tự -> switch rất hợp
void xuLyLenh(char lenh) {
    std::cout << "  Lệnh '" << lenh << "': ";
    switch (lenh) {
        case 'F': std::cout << "robot đi thẳng\n";  break;
        case 'B': std::cout << "robot đi lùi\n";    break;
        case 'L':
        case 'l':                                   // nhiều case dùng chung một xử lý (fall-through)
            std::cout << "rẽ trái\n";               break;
        case 'S': std::cout << "dừng\n";            break;
        default:  std::cout << "không hiểu lệnh\n"; break;
    }
}

enum class CheDo { TuDong, ThuCong, TietKiem };

int main() {
    std::cout << "== if / else if / else ==\n";
    for (float t : {15.0f, 25.0f, 31.5f, 40.0f}) xuLyNhietDo(t);

    std::cout << "\n== switch ==\n";
    for (char c : {'F', 'l', 'S', 'X'}) xuLyLenh(c);

    std::cout << "\n== switch với enum class ==\n";
    CheDo cheDo = CheDo::TietKiem;
    switch (cheDo) {
        case CheDo::TuDong:   std::cout << "  Tự động\n"; break;
        case CheDo::ThuCong:  std::cout << "  Thủ công\n"; break;
        case CheDo::TietKiem: std::cout << "  Tiết kiệm pin: giảm độ sáng màn hình\n"; break;
    }

    std::cout << "\n== if có khởi tạo (C++17) ==\n";
    if (int adc = 3100; adc > 3000) {      // biến adc chỉ sống trong if/else này
        std::cout << "  ADC = " << adc << " > 3000: đất khô, bật bơm\n";
    }

    std::cout << "\n== Bẫy thường gặp ==\n";
    int x = 0;
    if (x = 5) {                           // GÁN chứ không phải SO SÁNH! luôn đúng (g++ -Wall sẽ cảnh báo)
        std::cout << "  if (x = 5) luôn chạy vào đây, x giờ = " << x << "\n";
    }
}
