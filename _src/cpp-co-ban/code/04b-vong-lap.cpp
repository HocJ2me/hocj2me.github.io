// Vòng lặp: for, while, do-while, range-for, break/continue – và vòng loop() "không chặn" kiểu Arduino
#include <iostream>

// Giả lập millis() của Arduino: mỗi lần gọi thời gian trôi thêm 100 ms
unsigned long thoiGian = 0;
unsigned long millis() { return thoiGian += 100; }

int main() {
    std::cout << "== for: đếm biết trước số lần ==\n  ";
    for (int i = 1; i <= 5; i++) std::cout << i << " ";
    std::cout << "\n";

    std::cout << "\n== while: lặp khi điều kiện còn đúng ==\n";
    int pin = 100;
    int phut = 0;
    while (pin > 20) {        // dùng tới khi pin xuống 20%
        pin -= 15;
        phut += 30;
    }
    std::cout << "  Sau " << phut << " phút pin còn " << pin << "%\n";

    std::cout << "\n== do-while: chạy ít nhất 1 lần ==\n";
    int lanThu = 0;
    bool ketNoi = false;
    do {
        lanThu++;
        ketNoi = (lanThu == 3);   // giả sử lần thứ 3 kết nối WiFi thành công
        std::cout << "  Thử kết nối WiFi lần " << lanThu << (ketNoi ? ": OK\n" : ": thất bại\n");
    } while (!ketNoi && lanThu < 5);

    std::cout << "\n== range-for: duyệt mọi phần tử ==\n  ";
    int docCamBien[] = {512, 530, 498, 1023, 505};
    long tong = 0;
    for (int v : docCamBien) tong += v;
    std::cout << "Trung bình = " << tong / 5 << "\n";

    std::cout << "\n== break & continue ==\n  ";
    for (int v : docCamBien) {
        if (v == 1023) { std::cout << "[nhiễu, bỏ qua] "; continue; }   // bỏ qua lượt này
        if (v < 500)   { std::cout << v << " [< 500, dừng] "; break; }   // thoát hẳn vòng lặp
        std::cout << v << " ";
    }
    std::cout << "\n";

    std::cout << "\n== Lồng nhau: vẽ ma trận LED 3x5 ==\n";
    for (int hang = 0; hang < 3; hang++) {
        std::cout << "  ";
        for (int cot = 0; cot < 5; cot++) std::cout << ((hang + cot) % 2 ? "○ " : "● ");
        std::cout << "\n";
    }

    std::cout << "\n== Vòng loop() không chặn (non-blocking) bằng millis() ==\n";
    // Thay vì delay(500) làm treo cả chương trình, ta kiểm tra "đã đủ thời gian chưa?"
    unsigned long lanCuoiNhay = 0;
    bool led = false;
    for (int vong = 0; vong < 25; vong++) {        // giả lập 25 lần chạy loop()
        unsigned long now = millis();
        if (now - lanCuoiNhay >= 500) {
            lanCuoiNhay = now;
            led = !led;
            std::cout << "  t=" << now << "ms: LED " << (led ? "BẬT" : "TẮT") << "\n";
        }
        // ... các việc khác (đọc nút, cảm biến) vẫn chạy mỗi vòng
    }
}
