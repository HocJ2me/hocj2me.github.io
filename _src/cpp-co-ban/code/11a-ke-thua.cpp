// Tính kế thừa: lớp cha / lớp con, protected, thứ tự constructor-destructor, gọi hàm lớp cha
#include <iostream>
#include <string>

class CamBien {                                   // lớp CHA (base class)
public:
    CamBien(std::string ten, int chan, int giaLap) : ten_(std::move(ten)), chan_(chan), giaLap_(giaLap) {
        std::cout << "  CamBien() " << ten_ << "\n";
    }
    ~CamBien() { std::cout << "  ~CamBien() " << ten_ << "\n"; }

    void moTa() const { std::cout << "  " << ten_ << " nối chân " << chan_ << "\n"; }
    int docThoTho() const { return giaLap_; }     // giả lập analogRead (ADC 10 bit, 0..1023)

protected:                                        // lớp con dùng được, bên ngoài thì không
    std::string ten_;
    int chan_;
private:
    int giaLap_;
};

class CamBienNhiet : public CamBien {             // lớp CON kế thừa public
public:
    CamBienNhiet(int chan) : CamBien("LM35", chan, 88) {   // gọi constructor lớp cha trước
        std::cout << "  CamBienNhiet()\n";
    }
    ~CamBienNhiet() { std::cout << "  ~CamBienNhiet()\n"; }

    float docC() const {                          // thêm chức năng mới
        return docThoTho() * 3.3f / 1023 * 100;   // dùng lại hàm của lớp cha
    }
    void moTa() const {                           // che (hide) hàm cùng tên của lớp cha
        CamBien::moTa();                          // vẫn gọi được bản của lớp cha
        std::cout << "  -> loại cảm biến nhiệt, 10 mV/°C, ten_ (protected) = " << ten_ << "\n";
    }
};

class CamBienAnhSang : public CamBien {
public:
    CamBienAnhSang(int chan) : CamBien("LDR", chan, 512) {}
    bool troiToi() const { return docThoTho() < 600; }
};

// Đa kế thừa: một lớp có nhiều lớp cha (dùng thận trọng)
class CoTheGuiWifi { public: void gui(const std::string& s) const { std::cout << "  WiFi gửi: " << s << "\n"; } };
class TramThoiTiet : public CamBienNhiet, public CoTheGuiWifi {
public:
    TramThoiTiet() : CamBienNhiet(34) {}
    void baoCao() const { gui("T=" + std::to_string(int(docC())) + "C"); }
};

int main() {
    std::cout << "== Tạo đối tượng lớp con: constructor CHA chạy trước ==\n";
    {
        CamBienNhiet lm35(36);
        lm35.moTa();
        std::cout << "  Nhiệt độ: " << lm35.docC() << "°C\n";
        // lm35.ten_ = "x";     // LỖI: protected không truy cập được từ bên ngoài
        std::cout << "== Ra khỏi khối: destructor CON chạy trước ==\n";
    }

    std::cout << "\n== Lớp con khác cùng lớp cha ==\n";
    CamBienAnhSang ldr(39);
    ldr.moTa();
    std::cout << "  Trời tối? " << std::boolalpha << ldr.troiToi() << "\n";

    std::cout << "\n== Đa kế thừa ==\n";
    TramThoiTiet tram;
    tram.baoCao();
    std::cout << "\n== Hết main ==\n";
}
