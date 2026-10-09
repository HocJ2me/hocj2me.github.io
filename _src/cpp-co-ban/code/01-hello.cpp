// Chương trình C++ đầu tiên.
// Biên dịch:  g++ -std=c++17 01-hello.cpp -o hello
// Chạy:       ./hello        (Windows: hello.exe)

#include <iostream>     // chỉ thị tiền xử lý: chèn thư viện vào/ra (cout, cin)

/*
   Chú thích nhiều dòng.
   Mọi chương trình C++ bắt đầu chạy từ hàm main().
*/
int main() {
    std::cout << "Xin chào, C++!" << std::endl;   // in ra màn hình rồi xuống dòng

    // Mỗi câu lệnh kết thúc bằng dấu chấm phẩy ;
    // Khối lệnh được bao bởi cặp ngoặc nhọn { }
    int namHoc = 2026;
    std::cout << "Năm học: " << namHoc << "\n";

    std::cout << "C++ chạy trên: máy tính, Arduino, ESP32, STM32..." << '\n';

    return 0;   // 0 = chương trình kết thúc thành công
}
