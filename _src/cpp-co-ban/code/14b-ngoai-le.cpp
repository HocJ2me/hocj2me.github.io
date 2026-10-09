// Xử lý ngoại lệ: try / catch / throw, lớp ngoại lệ riêng – và cách thay thế khi firmware tắt exception
#include <iostream>
#include <optional>
#include <stdexcept>
#include <string>
#include <vector>

class LoiCamBien : public std::runtime_error {             // ngoại lệ tự định nghĩa
public:
    LoiCamBien(const std::string& ten, int maLoi)
        : std::runtime_error("Cảm biến " + ten + " lỗi mã " + std::to_string(maLoi)), maLoi(maLoi) {}
    int maLoi;
};

float docNhietDo(int lanThu) {
    if (lanThu == 2) throw LoiCamBien("DHT22", 4);         // NÉM ngoại lệ
    if (lanThu == 3) throw std::out_of_range("giá trị ngoài dải -40..80");
    return 27.5f + lanThu;
}

int chia(int a, int b) {
    if (b == 0) throw std::invalid_argument("chia cho 0");
    return a / b;
}

// Cách KHÔNG dùng exception (phổ biến trong firmware biên dịch với -fno-exceptions)
std::optional<float> docNhietDoAnToan(int lanThu) {
    if (lanThu == 2) return std::nullopt;                  // "không có giá trị" = lỗi
    return 27.5f + lanThu;
}

int main() {
    std::cout << "== try / catch nhiều loại ngoại lệ ==\n";
    for (int i = 1; i <= 4; i++) {
        try {
            float t = docNhietDo(i);
            std::cout << "  lần " << i << ": " << t << "°C\n";
        } catch (const LoiCamBien& e) {                    // bắt loại cụ thể trước
            std::cout << "  lần " << i << ": " << e.what() << " -> khởi động lại cảm biến\n";
        } catch (const std::exception& e) {                // rồi tới loại tổng quát
            std::cout << "  lần " << i << ": lỗi chung: " << e.what() << "\n";
        }
    }

    std::cout << "\n== Ngoại lệ của thư viện chuẩn ==\n";
    try {
        std::vector<int> v = {1, 2, 3};
        int x = v.at(10);                                  // ném ngoại lệ ở đây, dòng dưới không chạy
        std::cout << "  v.at(10) = " << x << "\n";
    } catch (const std::out_of_range&) {
        std::cout << "  v.at(10) ném std::out_of_range\n";
    }
    try {
        std::stoi("abc");
    } catch (const std::invalid_argument&) {
        std::cout << "  stoi(\"abc\") ném std::invalid_argument\n";
    }
    try {
        std::cout << "  chia(10, 2) = " << chia(10, 2) << "\n";
        int kq = chia(1, 0);
        std::cout << "  chia(1, 0) = " << kq << "\n";
    } catch (const std::invalid_argument& e) {
        std::cout << "  bắt được: " << e.what() << "\n";
    }

    std::cout << "\n== Không dùng exception: std::optional ==\n";
    for (int i = 1; i <= 2; i++) {
        if (auto t = docNhietDoAnToan(i)) std::cout << "  lần " << i << ": " << *t << "°C\n";
        else                              std::cout << "  lần " << i << ": đọc lỗi, dùng giá trị cũ\n";
    }
}
