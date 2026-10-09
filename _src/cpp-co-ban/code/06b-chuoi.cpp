// Chuỗi: chuỗi kiểu C (char[]) và std::string – kèm ví dụ phân tích lệnh nhận từ Serial
#include <cstdio>
#include <cstring>
#include <iostream>
#include <string>

int main() {
    std::cout << "== Chuỗi kiểu C: mảng char kết thúc bằng '\\0' ==\n";
    char ten[16] = "ESP32";                 // 5 ký tự + '\0' = 6 byte được dùng
    std::cout << "  ten = " << ten << ", strlen = " << std::strlen(ten) << ", sizeof = " << sizeof(ten) << "\n";
    std::strcat(ten, "-S3");                // nối chuỗi (PHẢI đủ chỗ, nếu không sẽ tràn bộ đệm!)
    std::cout << "  sau strcat: " << ten << "\n";
    std::cout << "  strcmp(\"abc\", \"abd\") = " << std::strcmp("abc", "abd") << " (âm: abc đứng trước)\n";

    char buf[32];
    int nhiet = 28, am = 65;
    // snprintf: định dạng chuỗi AN TOÀN, không bao giờ ghi quá kích thước buf
    std::snprintf(buf, sizeof(buf), "T=%dC H=%d%%", nhiet, am);
    std::cout << "  snprintf -> \"" << buf << "\"\n";
    char nho[8];
    int canGhi = std::snprintf(nho, sizeof(nho), "Xin chao cac ban");
    std::cout << "  Bộ đệm 8 byte chỉ giữ: \"" << nho << "\" (cần " << canGhi << " ký tự)\n";

    std::cout << "\n== std::string: tự quản lý bộ nhớ, dễ dùng ==\n";
    std::string s = "Hello";
    s += ", BKSTAR";                        // nối
    std::cout << "  s = " << s << ", length = " << s.length() << "\n";
    std::cout << "  s.substr(7, 6) = " << s.substr(7, 6) << "\n";
    std::cout << "  s.find(\"BK\") = " << s.find("BK") << "\n";
    s.replace(0, 5, "Xin chao");
    std::cout << "  sau replace: " << s << "\n";
    std::cout << "  so sánh == : " << std::boolalpha << (std::string("on") == "on") << "\n";

    std::cout << "\n== Chuyển đổi số <-> chuỗi ==\n";
    std::string soChuoi = std::to_string(3.5);
    int so = std::stoi("123") + 1;
    float f = std::stof("27.75");
    std::cout << "  to_string(3.5) = " << soChuoi << ", stoi(\"123\")+1 = " << so << ", stof = " << f << "\n";

    std::cout << "\n== Phân tích lệnh dạng \"TEN:GIA_TRI\" nhận qua Serial ==\n";
    for (std::string lenh : {"LED:1", "SERVO:90", "SPEED:255", "SAI_CU_PHAP"}) {
        size_t pos = lenh.find(':');
        if (pos == std::string::npos) {
            std::cout << "  \"" << lenh << "\" -> lỗi cú pháp\n";
            continue;
        }
        std::string ten = lenh.substr(0, pos);
        int giaTri = std::stoi(lenh.substr(pos + 1));
        std::cout << "  \"" << lenh << "\" -> thiết bị " << ten << ", giá trị " << giaTri << "\n";
    }

    std::cout << "\n== Lưu ý tiếng Việt: length() đếm BYTE (UTF-8), không phải số chữ ==\n";
    std::string viet = "Việt";
    std::cout << "  \"Việt\" có 4 chữ nhưng length() = " << viet.length() << "\n";
}
