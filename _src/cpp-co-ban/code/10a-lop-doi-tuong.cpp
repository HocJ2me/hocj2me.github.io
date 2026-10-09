// Lớp & đối tượng, tính bao đóng (encapsulation): private/public, constructor, destructor, getter/setter
#include <iostream>
#include <string>

class Led {
public:
    // Constructor: chạy khi đối tượng được tạo. Dùng danh sách khởi tạo ": pin_(pin), ..."
    Led(int pin, std::string ten = "LED") : pin_(pin), ten_(std::move(ten)) {
        soLuong++;
        std::cout << "  [tạo] " << ten_ << " ở chân " << pin_ << "\n";
    }
    // Destructor: chạy khi đối tượng bị huỷ (ra khỏi phạm vi)
    ~Led() {
        soLuong--;
        std::cout << "  [huỷ] " << ten_ << "\n";
    }

    void bat()  { trangThai_ = true;  doSang_ = 255; }
    void tat()  { trangThai_ = false; doSang_ = 0; }

    // Setter có KIỂM TRA dữ liệu – lý do chính của bao đóng
    bool datDoSang(int giaTri) {
        if (giaTri < 0 || giaTri > 255) return false;   // từ chối giá trị sai
        doSang_ = giaTri;
        trangThai_ = giaTri > 0;
        return true;
    }

    // Getter là hàm const: hứa không sửa đối tượng
    int doSang() const { return doSang_; }
    bool dangBat() const { return trangThai_; }
    void inTrangThai() const {
        std::cout << "  " << ten_ << "(chân " << pin_ << "): " << (trangThai_ ? "BẬT" : "TẮT")
                  << ", độ sáng " << doSang_ << "\n";
    }

    static int soLuong;              // thành viên static: dùng chung cho MỌI đối tượng của lớp

private:                             // bên ngoài không truy cập trực tiếp được
    const int pin_;                  // const: chân cố định suốt đời đối tượng
    std::string ten_;
    bool trangThai_ = false;         // giá trị mặc định
    int doSang_ = 0;
};
int Led::soLuong = 0;                // định nghĩa thành viên static

int main() {
    std::cout << "== Tạo đối tượng ==\n";
    Led ledDo(13, "LED đỏ");
    Led ledXanh(12, "LED xanh");
    std::cout << "  Số LED đang tồn tại: " << Led::soLuong << "\n";

    std::cout << "\n== Gọi phương thức ==\n";
    ledDo.bat();
    ledXanh.datDoSang(80);
    ledDo.inTrangThai();
    ledXanh.inTrangThai();

    std::cout << "\n== Bao đóng bảo vệ dữ liệu ==\n";
    // ledXanh.doSang_ = 999;        // LỖI biên dịch: doSang_ là private
    bool ok = ledXanh.datDoSang(999);
    std::cout << "  datDoSang(999) -> " << (ok ? "chấp nhận" : "từ chối") << ", độ sáng vẫn = " << ledXanh.doSang() << "\n";

    std::cout << "\n== Vòng đời: đối tượng trong khối {} bị huỷ khi ra khỏi khối ==\n";
    {
        Led tam(2, "LED tạm");
        std::cout << "  Số LED: " << Led::soLuong << "\n";
    }
    std::cout << "  Số LED sau khối: " << Led::soLuong << "\n";

    std::cout << "\n== Kết thúc main: các đối tượng còn lại bị huỷ theo thứ tự NGƯỢC lúc tạo ==\n";
}
