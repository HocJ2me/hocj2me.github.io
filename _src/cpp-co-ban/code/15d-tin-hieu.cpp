// Xử lý tín hiệu (signal): hệ điều hành báo sự kiện bất đồng bộ cho chương trình
// Ý tưởng rất giống NGẮT (interrupt) trên vi điều khiển: handler phải ngắn, chỉ đặt cờ.
#include <csignal>
#include <iostream>

volatile std::sig_atomic_t coDung = 0;      // kiểu an toàn để ghi trong signal handler
volatile std::sig_atomic_t soLanNhan = 0;

void xuLyTinHieu(int maTinHieu) {           // signal handler: KHÔNG in, KHÔNG cấp phát ở đây
    soLanNhan++;
    if (maTinHieu == SIGINT) coDung = 1;
}

int main() {
    std::signal(SIGINT, xuLyTinHieu);       // đăng ký: khi nhấn Ctrl+C -> gọi xuLyTinHieu
    std::signal(SIGTERM, xuLyTinHieu);

    std::cout << "== Vòng lặp chính chạy tới khi nhận SIGINT ==\n";
    for (int vong = 1; !coDung; vong++) {
        std::cout << "  vòng " << vong << ": đọc cảm biến, cập nhật màn hình\n";
        if (vong == 3) {
            std::cout << "  (giả lập người dùng nhấn Ctrl+C)\n";
            std::raise(SIGINT);              // tự gửi tín hiệu cho chính chương trình
        }
    }
    std::cout << "  Nhận tín hiệu " << soLanNhan << " lần -> lưu dữ liệu, đóng file, thoát an toàn\n";

    std::cout << "\n== Một số tín hiệu chuẩn ==\n";
    std::cout << "  SIGINT  = " << SIGINT  << "  ngắt từ bàn phím (Ctrl+C)\n";
    std::cout << "  SIGTERM = " << SIGTERM << " yêu cầu kết thúc\n";
    std::cout << "  SIGSEGV = " << SIGSEGV << " truy cập bộ nhớ sai (con trỏ hỏng)\n";
    std::cout << "  SIGFPE  = " << SIGFPE  << "  lỗi số học (chia nguyên cho 0)\n";
    std::cout << "  SIGABRT = " << SIGABRT << " abort()\n";

    std::signal(SIGINT, SIG_DFL);            // trả về xử lý mặc định
    return 0;
}
