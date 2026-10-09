// Bài 7 – Đảo ưu tiên (priority inversion) và kế thừa ưu tiên (priority inheritance).
// Thap (1) giữ khoá -> Cao (3) phải chờ khoá -> Vua (2) chen ngang Thap, làm Cao chờ lâu vô lý.
// Binary semaphore: KHÔNG kế thừa ưu tiên.  Mutex: Thap được tạm nâng lên ưu tiên 3.
#include "sim.h"
#include "semphr.h"

SemaphoreHandle_t khoa;
TickType_t batDau;

void taskThap(void*) {
    xSemaphoreTake(khoa, portMAX_DELAY);
    LOG("  Thap  (ƯT 1) lấy khoá, ghi thẻ SD 100 ms");
    for (int i = 0; i < 100; i++) {
        banTinhToan(1);
        if (i == 50) LOG("  Thap  đang giữ khoá, ưu tiên hiện tại = %u", (unsigned)uxTaskPriorityGet(nullptr));
    }
    LOG("  Thap  trả khoá");
    xSemaphoreGive(khoa);
    vTaskDelete(nullptr);
}

void taskCao(void*) {
    vTaskDelay(pdMS_TO_TICKS(10));
    LOG("Cao     (ƯT 3) cần khoá -> phải chờ Thap");
    xSemaphoreTake(khoa, portMAX_DELAY);
    LOG("Cao     có khoá sau khi chờ %lu ms", (unsigned long)(xTaskGetTickCount() - batDau - 10));
    xSemaphoreGive(khoa);
    vTaskDelete(nullptr);
}

void taskVua(void*) {
    vTaskDelay(pdMS_TO_TICKS(20));
    LOG(" Vua    (ƯT 2) không cần khoá, chạy 200 ms");
    banTinhToan(200);
    LOG(" Vua    xong");
    vTaskDelete(nullptr);
}

void chayThuNghiem(void* p) {
    for (int lan = 0; lan < 2; lan++) {
        bool dungMutex = (lan == 1);
        khoa = dungMutex ? xSemaphoreCreateMutex() : xSemaphoreCreateBinary();
        if (!dungMutex) xSemaphoreGive(khoa);       // binary tạo ra ở trạng thái rỗng
        LOG("========== Dùng %s ==========", dungMutex ? "MUTEX (có kế thừa ưu tiên)" : "BINARY SEMAPHORE (không kế thừa)");
        batDau = xTaskGetTickCount();
        xTaskCreate(taskThap, "Thap", 512, nullptr, 1, nullptr);
        xTaskCreate(taskCao,  "Cao",  512, nullptr, 3, nullptr);
        xTaskCreate(taskVua,  "Vua",  512, nullptr, 2, nullptr);
        vTaskDelay(pdMS_TO_TICKS(450));
        vSemaphoreDelete(khoa);
    }
    (void)p;
    ket_thuc();
}

int main() {
    xTaskCreate(chayThuNghiem, "DieuPhoi", 1024, nullptr, 4, nullptr);
    vTaskStartScheduler();
}
