// Bài 8 – Direct-to-task notification dùng như binary semaphore và counting semaphore.
// Mỗi task có sẵn một "hộp thư" 32 bit: không cần tạo đối tượng, nhanh hơn và tốn ít RAM hơn semaphore.
#include "sim.h"
#include "semphr.h"

TaskHandle_t hXuLy = nullptr;

uint32_t isrAdcXong() {                              // ngắt "ADC chuyển đổi xong"
    BaseType_t c = pdFALSE;
    vTaskNotifyGiveFromISR(hXuLy, &c);               // tăng giá trị notification của task lên 1
    return c;
}

void taskXuLy(void*) {
    LOG("== Như BINARY semaphore: ulTaskNotifyTake(pdTRUE, ...) xoá về 0 sau khi nhận ==");
    for (int i = 0; i < 2; i++) {
        uint32_t n = ulTaskNotifyTake(pdTRUE, portMAX_DELAY);
        LOG("XuLy  thức dậy, giá trị notification = %lu -> đọc ADC", (unsigned long)n);
    }
    LOG("== Như COUNTING semaphore: ulTaskNotifyTake(pdFALSE, ...) giảm đi 1 mỗi lần ==");
    vTaskDelay(pdMS_TO_TICKS(200));                  // trong lúc ngủ, 3 ngắt dồn lại
    for (int i = 0; i < 3; i++) {
        uint32_t n = ulTaskNotifyTake(pdFALSE, 0);
        LOG("XuLy  xử lý 1 sự kiện (còn lại %lu)", (unsigned long)(n - 1));
    }
    LOG("Kích thước: một binary semaphore ~%u byte RAM; notification: 0 byte thêm (nằm sẵn trong TCB)",
        (unsigned)sizeof(StaticSemaphore_t));
    ket_thuc();
}

void taskPhanCung(void*) {
    vTaskDelay(pdMS_TO_TICKS(100)); LOG("[ngắt] ADC xong"); phatNgat(3);
    vTaskDelay(pdMS_TO_TICKS(100)); LOG("[ngắt] ADC xong"); phatNgat(3);
    vTaskDelay(pdMS_TO_TICKS(100));
    for (int i = 0; i < 3; i++) { LOG("[ngắt] ADC xong (dồn)"); phatNgat(3); vTaskDelay(pdMS_TO_TICKS(20)); }
    vTaskDelete(nullptr);
}

int main() {
    dangKyNgat(3, isrAdcXong);
    xTaskCreate(taskXuLy,     "XuLy",     1024, nullptr, 2, &hXuLy);
    xTaskCreate(taskPhanCung, "PhanCung", 512,  nullptr, 3, nullptr);
    vTaskStartScheduler();
}
