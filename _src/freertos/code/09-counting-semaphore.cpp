// Bài 6 – Counting semaphore: quản lý một NHÓM tài nguyên giống nhau (ở đây: 2 kênh DMA / 2 chỗ sạc)
// và đếm sự kiện (nhiều ngắt dồn lại không bị mất).
#include "sim.h"
#include "semphr.h"

SemaphoreHandle_t semKenh;                            // 2 kênh truyền dữ liệu dùng chung

void taskGuiDuLieu(void* p) {
    const char* ten = static_cast<const char*>(p);
    LOG("%s xin một kênh (còn %u kênh rảnh)", ten, (unsigned)uxSemaphoreGetCount(semKenh));
    xSemaphoreTake(semKenh, portMAX_DELAY);           // giảm bộ đếm; nếu = 0 thì chờ
    LOG("%s ĐƯỢC cấp kênh, gửi dữ liệu 300 ms", ten);
    vTaskDelay(pdMS_TO_TICKS(300));
    LOG("%s trả kênh", ten);
    xSemaphoreGive(semKenh);                          // tăng bộ đếm
    vTaskDelete(nullptr);
}

// ===== Đếm sự kiện: encoder phát nhiều xung liên tiếp =====
SemaphoreHandle_t semXung;
uint32_t isrEncoder() {
    BaseType_t c = pdFALSE;
    xSemaphoreGiveFromISR(semXung, &c);
    return c;
}

void taskDemXung(void*) {
    vTaskDelay(pdMS_TO_TICKS(800));
    LOG("== Phần 2: 5 xung encoder tới dồn dập trong lúc task đang bận ==");
    for (int i = 0; i < 5; i++) phatNgat(3);
    vTaskDelay(pdMS_TO_TICKS(10));
    int dem = 0;
    while (xSemaphoreTake(semXung, 0) == pdTRUE) dem++;
    LOG("DemXung  xử lý được %d/5 xung (counting semaphore không làm mất xung)", dem);
    ket_thuc();
}

int main() {
    semKenh = xSemaphoreCreateCounting(2, 2);          // tối đa 2, ban đầu 2 (cả hai kênh rảnh)
    semXung = xSemaphoreCreateCounting(10, 0);         // đếm sự kiện: ban đầu 0
    dangKyNgat(3, isrEncoder);
    static const char* ten[] = {"Task A", "Task B", "Task C", "Task D"};
    for (int i = 0; i < 4; i++) xTaskCreate(taskGuiDuLieu, ten[i], 512, (void*)ten[i], 2, nullptr);
    xTaskCreate(taskDemXung, "DemXung", 512, nullptr, 1, nullptr);
    vTaskStartScheduler();
}
