// Bài 1 – Vì sao cần RTOS? Mô phỏng chương trình "siêu vòng lặp" (super loop) kiểu Arduino
// KHÔNG dùng FreeRTOS: mỗi việc dùng delay() chặn -> nút nhấn bị bỏ lỡ.
#include <cstdio>

unsigned long thoiGian = 0;                       // đồng hồ giả lập (ms)
void delayMs(unsigned long ms) { thoiGian += ms; } // delay(): CPU đứng chờ, không làm gì khác được

// Nút được nhấn tại các thời điểm này (mỗi lần nhấn giữ 50 ms)
const unsigned long LAN_NHAN[] = {120, 950, 1430, 2210};
bool nutDangNhan() {
    for (unsigned long t : LAN_NHAN)
        if (thoiGian >= t && thoiGian < t + 50) return true;
    return false;
}

int main() {
    int phatHien = 0;
    std::printf("== Siêu vòng lặp với delay() ==\n");
    while (thoiGian < 2500) {                     // loop()
        if (nutDangNhan()) { phatHien++; std::printf("[%4lu ms] phát hiện nút nhấn\n", thoiGian); }
        std::printf("[%4lu ms] đọc cảm biến DHT22 (mất 250 ms)\n", thoiGian);
        delayMs(250);
        std::printf("[%4lu ms] cập nhật màn hình LCD (mất 200 ms)\n", thoiGian);
        delayMs(200);
    }
    std::printf("Nhấn 4 lần, chỉ phát hiện %d lần -> bỏ lỡ %d lần!\n", phatHien, 4 - phatHien);
    std::printf("RTOS giải quyết: mỗi việc là một TASK, task đọc nút có ưu tiên cao được chạy ngay.\n");
}
