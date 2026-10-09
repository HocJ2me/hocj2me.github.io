// Bài 3 – vTaskDelay vs vTaskDelayUntil (chu kỳ chính xác), vTaskSuspend/Resume, đổi ưu tiên lúc chạy
#include "sim.h"

void taskLayMau(void*) {
    LOG("== Cách 1: vTaskDelay(100) sau khi xử lý 30 ms ==");
    for (int i = 0; i < 4; i++) {
        LOG("vTaskDelay      lấy mẫu lần %d", i);
        banTinhToan(30);                             // xử lý mất 30 ms
        vTaskDelay(pdMS_TO_TICKS(100));              // nghỉ 100 ms TÍNH TỪ BÂY GIỜ -> chu kỳ thực 130 ms (trôi dần)
    }
    LOG("== Cách 2: vTaskDelayUntil(&moc, 100) ==");
    TickType_t moc = xTaskGetTickCount();
    for (int i = 0; i < 4; i++) {
        LOG("vTaskDelayUntil lấy mẫu lần %d", i);
        banTinhToan(30);
        vTaskDelayUntil(&moc, pdMS_TO_TICKS(100));   // đánh thức đúng moc + 100 -> chu kỳ đúng 100 ms
    }
    vTaskDelete(nullptr);
}

TaskHandle_t hNhay = nullptr;
void taskNhayLed(void*) {
    vTaskDelay(pdMS_TO_TICKS(1000));
    for (;;) {
        LOG("  NhayLed  nháy (ưu tiên %u)", (unsigned)uxTaskPriorityGet(nullptr));
        vTaskDelay(pdMS_TO_TICKS(150));
    }
}

void taskDieuKhien(void*) {
    vTaskDelay(pdMS_TO_TICKS(1320));
    LOG("DieuKhien  -> vTaskSuspend(NhayLed): tạm dừng");
    vTaskSuspend(hNhay);
    vTaskDelay(pdMS_TO_TICKS(400));
    LOG("DieuKhien  -> vTaskResume(NhayLed) và nâng ưu tiên lên 3");
    vTaskPrioritySet(hNhay, 3);
    vTaskResume(hNhay);
    vTaskDelay(pdMS_TO_TICKS(320));
    ket_thuc();
}

int main() {
    xTaskCreate(taskLayMau,    "LayMau",    512, nullptr, 2, nullptr);
    xTaskCreate(taskNhayLed,   "NhayLed",   512, nullptr, 1, &hNhay);
    xTaskCreate(taskDieuKhien, "DieuKhien", 512, nullptr, 4, nullptr);
    vTaskStartScheduler();
}
