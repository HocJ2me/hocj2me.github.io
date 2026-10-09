// Bài 2 – Task đầu tiên: tạo 2 task nháy 2 "LED" với chu kỳ khác nhau, chạy song song
#include "sim.h"

void taskLedDo(void* thamSo) {
    (void)thamSo;
    for (int i = 0; i < 4; i++) {                 // trên board thật là for (;;) – task không bao giờ return
        LOG("LED đỏ   %s", i % 2 ? "TẮT" : "BẬT");
        vTaskDelay(pdMS_TO_TICKS(500));           // nhường CPU 500 ms (KHÔNG chặn task khác như delay())
    }
    vTaskDelete(nullptr);                         // task tự xoá khi xong việc
}

void taskLedXanh(void* thamSo) {
    int chuKy = *static_cast<int*>(thamSo);       // nhận tham số qua con trỏ void*
    for (int i = 0; i < 6; i++) {
        LOG("LED xanh %s", i % 2 ? "TẮT" : "BẬT");
        vTaskDelay(pdMS_TO_TICKS(chuKy));
    }
    LOG("Hai task đã chạy song song xong");
    ket_thuc();
}

int main() {
    static int chuKyXanh = 300;                   // static: phải còn sống khi task chạy
    PRINT("Tạo task...");
    xTaskCreate(taskLedDo,   "LedDo",   configMINIMAL_STACK_SIZE, nullptr,    1, nullptr);
    xTaskCreate(taskLedXanh, "LedXanh", configMINIMAL_STACK_SIZE, &chuKyXanh, 1, nullptr);
    PRINT("Khởi động scheduler – từ đây FreeRTOS điều khiển CPU");
    vTaskStartScheduler();                        // không bao giờ trả về nếu đủ bộ nhớ
    PRINT("Không đủ heap để tạo idle task!");
}
