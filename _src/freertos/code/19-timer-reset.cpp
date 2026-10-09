// Bài 11 – Reset timer: tự tắt đèn nền LCD sau 1 giây KHÔNG có thao tác. Mỗi lần nhấn nút -> đếm lại từ đầu.
// Đây là cách làm "timeout không hoạt động" chuẩn trên thiết bị nhúng (màn hình, chế độ ngủ, watchdog mềm).
#include "sim.h"
#include "timers.h"

TimerHandle_t tmrDenNen;
bool denNenBat = false;

void cbTatDenNen(TimerHandle_t) {
    denNenBat = false;
    LOG("  [timer] 1000 ms không thao tác -> TẮT đèn nền LCD");
}

uint32_t isrNut() {                                     // nhấn nút: bật đèn nền + reset timer (bản FromISR)
    BaseType_t c = pdFALSE;
    denNenBat = true;
    xTimerResetFromISR(tmrDenNen, &c);                  // nếu timer đang dừng thì khởi động, đang chạy thì đếm lại
    return c;
}

void taskNguoiDung(void*) {
    const uint32_t lanNhan[] = {100, 600, 1100, 1500, 3200};
    TickType_t truoc = 0;
    for (uint32_t t : lanNhan) {
        vTaskDelay(pdMS_TO_TICKS(t - truoc));
        truoc = t;
        LOG("Nhấn nút -> bật đèn nền, đếm lại 1000 ms");
        phatNgat(3);
    }
    vTaskDelay(pdMS_TO_TICKS(1200));
    ket_thuc();
}

int main() {
    tmrDenNen = xTimerCreate("DenNen", pdMS_TO_TICKS(1000), pdFALSE, nullptr, cbTatDenNen);
    dangKyNgat(3, isrNut);
    xTaskCreate(taskNguoiDung, "NguoiDung", 512, nullptr, 1, nullptr);
    vTaskStartScheduler();
}
