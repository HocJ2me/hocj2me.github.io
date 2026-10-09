// Bộ tiền xử lý (preprocessor): #define, macro, biên dịch có điều kiện, macro có sẵn
// Chạy TRƯỚC khi biên dịch: chỉ thay thế văn bản, không hiểu kiểu dữ liệu.
#include <iostream>

#define LED_PIN 13                       // hằng kiểu C (C++ nên dùng constexpr)
#define BINH_PHUONG_SAI(x) x * x         // macro thiếu ngoặc -> bẫy!
#define BINH_PHUONG(x) ((x) * (x))
#define DEBUG 1                          // bật/tắt log khi biên dịch
#define BOARD_ESP32                      // chọn phần cứng

#if DEBUG
  #define LOG(msg) std::cout << "  [DEBUG " << __FILE__ << ":" << __LINE__ << "] " << msg << "\n"
#else
  #define LOG(msg)                       // bản phát hành: log biến mất hoàn toàn, không tốn byte nào
#endif

#ifdef BOARD_ESP32
  constexpr int ADC_MAX = 4095;          // 12 bit
  constexpr const char* TEN_BOARD = "ESP32";
#elif defined(BOARD_UNO)
  constexpr int ADC_MAX = 1023;          // 10 bit
  constexpr const char* TEN_BOARD = "Arduino Uno";
#else
  #error "Chưa chọn board!"
#endif

#define CHUOI_HOA(x) #x                  // toán tử # biến tham số thành chuỗi
#define NOI(a, b) a##b                   // toán tử ## nối hai token

int main() {
    std::cout << "== #define hằng ==\n";
    std::cout << "  LED_PIN = " << LED_PIN << "\n";

    std::cout << "\n== Macro hàm và bẫy thiếu ngoặc ==\n";
    std::cout << "  BINH_PHUONG_SAI(2 + 3) = " << BINH_PHUONG_SAI(2 + 3) << "  (thành 2 + 3 * 2 + 3!)\n";
    std::cout << "  BINH_PHUONG(2 + 3)     = " << BINH_PHUONG(2 + 3) << "\n";

    std::cout << "\n== Biên dịch có điều kiện ==\n";
    std::cout << "  Board: " << TEN_BOARD << ", ADC_MAX = " << ADC_MAX << "\n";
    LOG("khởi động xong");

    std::cout << "\n== # và ## ==\n";
    int NOI(dem, 1) = 5;                 // tạo biến tên dem1
    std::cout << "  " << CHUOI_HOA(dem1) << " = " << dem1 << "\n";

    std::cout << "\n== Macro có sẵn ==\n";
    std::cout << "  __cplusplus = " << __cplusplus << " (201703 = C++17)\n";
    std::cout << "  __func__    = " << __func__ << "\n";
#ifdef __GNUC__
    std::cout << "  Trình biên dịch: GCC " << __GNUC__ << "\n";
#endif

    std::cout << "\n  Include guard trong file .h:\n"
                 "    #ifndef CAM_BIEN_H\n    #define CAM_BIEN_H\n    ...\n    #endif   (hoặc #pragma once)\n";
}
