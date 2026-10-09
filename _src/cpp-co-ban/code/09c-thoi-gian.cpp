// Ngày & giờ: <ctime> kiểu C và <chrono> kiểu C++
#include <chrono>
#include <ctime>
#include <iostream>
#include <thread>

int main() {
    std::cout << "== time_t: số giây kể từ 1/1/1970 (Unix time) ==\n";
    // Dùng một mốc cố định để ví dụ lần nào chạy cũng ra cùng kết quả.
    // Thực tế: std::time(nullptr) lấy giờ hiện tại; ESP32 đồng bộ giờ qua NTP rồi dùng y hệt.
    std::time_t t = 1760000000;
    std::tm utc = *std::gmtime(&t);
    char buf[64];
    std::strftime(buf, sizeof(buf), "%d/%m/%Y %H:%M:%S", &utc);
    std::cout << "  t = " << t << " -> " << buf << " (UTC)\n";
    std::cout << "  Thứ trong tuần (0 = CN): " << utc.tm_wday << ", ngày thứ " << utc.tm_yday + 1 << " trong năm\n";

    std::time_t gioVN = t + 7 * 3600;         // múi giờ Việt Nam UTC+7
    std::tm vn = *std::gmtime(&gioVN);
    std::strftime(buf, sizeof(buf), "%H:%M ngày %d/%m", &vn);
    std::cout << "  Giờ Việt Nam: " << buf << "\n";

    std::cout << "\n== Tính khoảng cách giữa hai ngày ==\n";
    std::tm ngayThi{};
    ngayThi.tm_year = 2026 - 1900; ngayThi.tm_mon = 11 - 1; ngayThi.tm_mday = 15;   // 15/11/2026
    std::tm homNay{};
    homNay.tm_year = 2026 - 1900; homNay.tm_mon = 10 - 1; homNay.tm_mday = 9;       // 09/10/2026
    double giay = std::difftime(std::mktime(&ngayThi), std::mktime(&homNay));
    std::cout << "  Từ 09/10 tới ngày thi 15/11 còn " << giay / 86400 << " ngày\n";

    std::cout << "\n== <chrono>: đơn vị thời gian an toàn kiểu ==\n";
    using namespace std::chrono;
    auto chuKy = milliseconds(1500);
    std::cout << "  1500 ms = " << duration_cast<seconds>(chuKy).count() << " s (cắt) = "
              << duration<double>(chuKy).count() << " s\n";
    auto tong = minutes(2) + seconds(30);
    std::cout << "  2 phút + 30 giây = " << tong.count() << " giây\n";

    std::cout << "\n== Đo thời gian thực thi (giống micros() trên Arduino) ==\n";
    auto batDau = steady_clock::now();
    std::this_thread::sleep_for(milliseconds(50));
    auto daQua = duration_cast<milliseconds>(steady_clock::now() - batDau).count();
    std::cout << "  sleep_for(50ms) mất khoảng " << (daQua >= 50 ? ">= 50" : "< 50") << " ms\n";
}
