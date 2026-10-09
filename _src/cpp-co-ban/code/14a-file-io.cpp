// File I/O và Stream: ghi/đọc file văn bản (CSV log), ghi thêm, file nhị phân
// (Trên ESP32 dùng y hệt với thẻ SD hoặc LittleFS qua thư viện File/FS)
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

struct BanGhi { int giay; float nhietDo; int doAm; };

int main() {
    std::cout << "== Ghi file CSV ==\n";
    {
        std::ofstream f("log.csv");                       // mở để GHI (xoá nội dung cũ)
        if (!f) { std::cerr << "Không mở được file\n"; return 1; }
        f << "giay,nhiet_do,do_am\n";
        BanGhi duLieu[] = {{0, 28.5f, 60}, {10, 28.9f, 61}, {20, 29.4f, 59}};
        for (const auto& b : duLieu) f << b.giay << "," << b.nhietDo << "," << b.doAm << "\n";
    }                                                     // ra khỏi khối -> file tự đóng (RAII)
    std::cout << "  đã ghi log.csv\n";

    std::cout << "\n== Ghi THÊM vào cuối file (append) ==\n";
    {
        std::ofstream f("log.csv", std::ios::app);
        f << 30 << "," << 30.1 << "," << 58 << "\n";
    }

    std::cout << "\n== Đọc lại từng dòng và phân tích CSV ==\n";
    std::ifstream in("log.csv");
    std::string dong;
    std::getline(in, dong);                               // bỏ dòng tiêu đề
    float tong = 0;
    int n = 0;
    while (std::getline(in, dong)) {
        std::stringstream ss(dong);
        std::string o;
        BanGhi b{};
        std::getline(ss, o, ','); b.giay = std::stoi(o);
        std::getline(ss, o, ','); b.nhietDo = std::stof(o);
        std::getline(ss, o, ','); b.doAm = std::stoi(o);
        std::cout << "  t=" << b.giay << "s  T=" << b.nhietDo << "  H=" << b.doAm << "\n";
        tong += b.nhietDo;
        n++;
    }
    std::cout << "  Nhiệt độ trung bình: " << tong / n << "\n";

    std::cout << "\n== File nhị phân: lưu cấu hình (giống EEPROM.put/get) ==\n";
    struct CauHinh { int nguong; float heSo; char wifi[16]; };
    CauHinh luu{32, 1.05f, "BKSTAR-Lab"};
    std::ofstream fb("config.bin", std::ios::binary);
    fb.write(reinterpret_cast<const char*>(&luu), sizeof(luu));
    fb.close();

    CauHinh doc{};
    std::ifstream fr("config.bin", std::ios::binary);
    fr.read(reinterpret_cast<char*>(&doc), sizeof(doc));
    std::cout << "  đọc lại: nguong=" << doc.nguong << ", heSo=" << doc.heSo << ", wifi=" << doc.wifi
              << " (" << fr.gcount() << " byte)\n";

    std::cout << "\n== Mở file không tồn tại ==\n";
    std::ifstream khong("khong_co.txt");
    std::cout << "  is_open() = " << std::boolalpha << khong.is_open() << " -> luôn kiểm tra!\n";
}
