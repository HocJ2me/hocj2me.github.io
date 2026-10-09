// Biến, phạm vi biến, hằng số, literal và modifier
#include <cstdint>
#include <iostream>

int soLanKhoiDong = 0;                    // biến TOÀN CỤC: sống suốt chương trình, mọi hàm thấy được

const int LED_PIN = 13;                   // hằng: không thể gán lại
constexpr uint32_t BAUD = 115200;         // hằng tính lúc BIÊN DỊCH
constexpr int TONG_CHAN = 2 * 20 + 4;     // biểu thức hằng – trình biên dịch tính sẵn = 44

void tangBien() {
    int cucBo = 0;                        // biến CỤC BỘ: tạo mới mỗi lần gọi hàm
    cucBo++;
    soLanKhoiDong++;
    std::cout << "  cucBo = " << cucBo << ", soLanKhoiDong = " << soLanKhoiDong << "\n";
}

int main() {
    std::cout << "== Phạm vi biến ==\n";
    tangBien();
    tangBien();

    int x = 10;
    {                                      // khối lệnh mới = phạm vi mới
        int x = 99;                        // biến che (shadow) x bên ngoài – nên tránh!
        int y = 5;
        std::cout << "  trong khối: x = " << x << ", y = " << y << "\n";
    }
    // std::cout << y;                     // LỖI: y đã ra khỏi phạm vi
    std::cout << "  ngoài khối: x = " << x << "\n";

    std::cout << "\n== Hằng ==\n";
    std::cout << "  LED_PIN = " << LED_PIN << ", BAUD = " << BAUD << ", TONG_CHAN = " << TONG_CHAN << "\n";
    // LED_PIN = 2;                        // LỖI biên dịch: không gán được hằng

    std::cout << "\n== Literal (cách viết hằng số) ==\n";
    int thapPhan = 255;
    int thapLucPhan = 0xFF;                // hệ 16 – hay dùng cho thanh ghi, mã màu
    int nhiPhan = 0b11111111;              // hệ 2 (C++14) – dễ nhìn từng bit
    int batPhan = 0377;                    // hệ 8 – số 0 đứng đầu! dễ nhầm
    std::cout << "  255 = 0xFF = 0b11111111 = 0377 ? "
              << (thapPhan == thapLucPhan && thapLucPhan == nhiPhan && nhiPhan == batPhan) << "\n";
    unsigned long trieu = 1'000'000UL;     // dấu ' phân cách chữ số (C++14), hậu tố UL
    float pi = 3.14159f;                   // hậu tố f = float
    std::cout << "  trieu = " << trieu << ", pi = " << pi << ", ký tự xuống dòng '\\n', tab '\\t'\n";

    std::cout << "\n== Modifier: signed / unsigned / short / long ==\n";
    unsigned int u = 0;
    u = u - 1;                             // không âm được -> quay vòng thành số rất lớn
    std::cout << "  unsigned 0 - 1 = " << u << "\n";
    signed char sc = -128;
    short s = 32767;
    long long ll = 9'000'000'000LL;
    std::cout << "  signed char = " << int(sc) << ", short = " << s << ", long long = " << ll << "\n";

    std::cout << "\n== auto: để trình biên dịch tự suy ra kiểu ==\n";
    auto nhietDo = 28.5;                   // double
    auto soCamBien = 4;                    // int
    std::cout << "  sizeof(nhietDo) = " << sizeof(nhietDo) << ", sizeof(soCamBien) = " << sizeof(soCamBien) << "\n";
}
