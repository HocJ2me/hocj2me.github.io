// Tính trừu tượng: lớp trừu tượng (hàm thuần ảo = 0) và interface
#include <cstdio>
#include <iostream>
#include <string>

// INTERFACE: chỉ có hàm thuần ảo – mô tả "làm được gì", không nói "làm thế nào"
class IHienThi {
public:
    virtual ~IHienThi() = default;
    virtual void xoa() = 0;
    virtual void inDong(int dong, const std::string& s) = 0;
};

class IGhiLog {
public:
    virtual ~IGhiLog() = default;
    virtual void ghi(const std::string& s) = 0;
};

// LỚP TRỪU TƯỢNG: có cả hàm thuần ảo lẫn code dùng chung
class CamBien {
public:
    virtual ~CamBien() = default;
    virtual float doc() = 0;                       // lớp con BẮT BUỘC cài đặt
    virtual std::string donVi() const = 0;
    std::string docChuoi() {                       // code chung, dùng hàm trừu tượng ở trên
        char buf[16];
        std::snprintf(buf, sizeof(buf), "%.1f", doc());
        return buf + donVi();
    }
};

// ===== Các lớp cụ thể =====
class Lcd1602 : public IHienThi {
public:
    void xoa() override { std::cout << "  [LCD] xoá màn hình\n"; }
    void inDong(int d, const std::string& s) override { std::cout << "  [LCD dòng " << d << "] " << s << "\n"; }
};
class SerialMonitor : public IHienThi, public IGhiLog {    // một lớp cài nhiều interface
public:
    void xoa() override {}
    void inDong(int d, const std::string& s) override { std::cout << "  [Serial] " << d << ": " << s << "\n"; }
    void ghi(const std::string& s) override { std::cout << "  [Serial LOG] " << s << "\n"; }
};
class Dht22 : public CamBien {
public:
    float doc() override { return 28.46f; }
    std::string donVi() const override { return "C"; }
};
class Bh1750 : public CamBien {
public:
    float doc() override { return 356.7f; }
    std::string donVi() const override { return " lux"; }
};

// Logic ứng dụng chỉ phụ thuộc vào TRỪU TƯỢNG -> đổi phần cứng không phải sửa hàm này
void capNhatManHinh(IHienThi& man, CamBien& nhiet, CamBien& anhSang) {
    man.xoa();
    man.inDong(0, "Nhiet do: " + nhiet.docChuoi());
    man.inDong(1, "Anh sang: " + anhSang.docChuoi());
}

int main() {
    Dht22 dht;
    Bh1750 bh;
    Lcd1602 lcd;
    SerialMonitor serial;

    std::cout << "== Cùng một hàm, hiển thị lên LCD ==\n";
    capNhatManHinh(lcd, dht, bh);
    std::cout << "\n== ... hoặc lên Serial Monitor, không sửa code ==\n";
    capNhatManHinh(serial, dht, bh);

    std::cout << "\n== Dùng qua interface khác ==\n";
    IGhiLog& log = serial;
    log.ghi("Khởi động xong");

    // CamBien cb;   // LỖI: không tạo được đối tượng từ lớp trừu tượng
    std::cout << "\n  Không thể tạo đối tượng CamBien trực tiếp vì nó có hàm thuần ảo.\n";
}
