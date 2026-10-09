// Lớp lưu trữ (storage class): auto, static, extern, mutable, thread_local – và từ khoá volatile
#include <iostream>

// static ở phạm vi file: biến/hàm chỉ thấy được trong file .cpp này (internal linkage)
static int demNoiBo = 0;

// extern: KHAI BÁO biến được ĐỊNH NGHĨA ở nơi khác (thường ở file .cpp khác).
// Ở đây định nghĩa ngay bên dưới để chương trình chạy được trong một file.
extern int soLanNhanNut;
int soLanNhanNut = 0;

int docCamBien() {
    static int lanGoi = 0;     // static CỤC BỘ: khởi tạo 1 lần, GIỮ giá trị giữa các lần gọi
    int tam = 0;               // biến tự động (automatic): tạo lại mỗi lần gọi
    lanGoi++;
    tam++;
    std::cout << "  docCamBien(): lanGoi = " << lanGoi << ", tam = " << tam << "\n";
    return lanGoi * 10;
}

class Led {
public:
    void bat() const {
        soLanTruyCap++;        // được phép sửa trong hàm const vì là mutable
        std::cout << "  LED bật (lần truy cập " << soLanTruyCap << ")\n";
    }
private:
    mutable int soLanTruyCap = 0;
};

// volatile: báo trình biên dịch "giá trị có thể bị thay đổi từ bên ngoài" (ngắt, phần cứng)
// -> không được tối ưu hoá bằng cách đọc từ thanh ghi CPU cũ, phải đọc lại bộ nhớ mỗi lần.
volatile bool coNgat = false;

void isrNutNhan() {            // giả lập hàm phục vụ ngắt (ISR)
    coNgat = true;
    soLanNhanNut++;
}

int main() {
    std::cout << "== static cục bộ ==\n";
    docCamBien();
    docCamBien();
    docCamBien();

    std::cout << "\n== static toàn cục & extern ==\n";
    demNoiBo += 5;
    isrNutNhan();
    isrNutNhan();
    std::cout << "  demNoiBo = " << demNoiBo << ", soLanNhanNut = " << soLanNhanNut << "\n";

    std::cout << "\n== mutable ==\n";
    const Led led;
    led.bat();
    led.bat();

    std::cout << "\n== volatile ==\n";
    if (coNgat) {
        coNgat = false;
        std::cout << "  Phát hiện ngắt từ nút nhấn -> xử lý trong loop()\n";
    }

    std::cout << "\n== thread_local ==\n";
    thread_local int moiLuongMotBan = 7;   // mỗi luồng có một bản riêng (xem bài Đa luồng)
    std::cout << "  moiLuongMotBan = " << moiLuongMotBan << "\n";
}
