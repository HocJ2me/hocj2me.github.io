// Bài 6 – Binary semaphore: "xử lý ngắt trì hoãn" (deferred interrupt processing).
// ISR chỉ báo hiệu (give) rồi thoát ngay; task xử lý (ưu tiên cao) làm phần việc nặng.
#include "sim.h"
#include "semphr.h"

SemaphoreHandle_t semNut;
volatile uint32_t soLanNgat = 0;

uint32_t isrNutNhan() {                              // ISR: thật ngắn, không in, không chờ
    soLanNgat++;
    BaseType_t canChuyen = pdFALSE;
    xSemaphoreGiveFromISR(semNut, &canChuyen);
    return canChuyen;                                // = portYIELD_FROM_ISR(canChuyen) trên board thật
}

void taskXuLyNut(void*) {
    for (;;) {
        if (xSemaphoreTake(semNut, pdMS_TO_TICKS(450)) == pdTRUE) {    // ngủ tới khi ISR give (tối đa 450 ms)
            LOG("XuLyNut  được đánh thức -> đọc chống dội, đổi chế độ quạt (việc nặng ở đây)");
        } else {
            LOG("XuLyNut  450 ms không có ai nhấn nút -> kết thúc ví dụ");
            ket_thuc();
        }
    }
}

void taskNen(void*) {
    for (;;) {
        banTinhToan(100);                            // task nền bận liên tục
        LOG("  Nen    đang tính toán...");
    }
}

void taskPhanCung(void*) {                           // giả lập người dùng nhấn nút
    const uint32_t thoiDiem[] = {250, 520, 900};
    TickType_t truoc = 0;
    for (uint32_t t : thoiDiem) {
        vTaskDelay(pdMS_TO_TICKS(t - truoc));
        truoc = t;
        LOG("[phần cứng] nút được nhấn -> phát ngắt");
        phatNgat(3);
    }
    vTaskDelete(nullptr);
}

int main() {
    semNut = xSemaphoreCreateBinary();               // tạo ra ở trạng thái "trống" (đã bị take)
    dangKyNgat(3, isrNutNhan);
    xTaskCreate(taskXuLyNut,  "XuLyNut",  512, nullptr, 3, nullptr);
    xTaskCreate(taskNen,      "Nen",      512, nullptr, 1, nullptr);
    xTaskCreate(taskPhanCung, "PhanCung", 512, nullptr, 4, nullptr);
    vTaskStartScheduler();
}
