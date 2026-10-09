// Bài 7 – Mutex bảo vệ tài nguyên dùng chung (màn hình LCD).
// Ghi một dòng lên LCD gồm nhiều bước; nếu task khác chen vào giữa -> màn hình bị lẫn chữ.
#include <cstring>
#include "sim.h"
#include "semphr.h"

char lcd[2][17];                                      // màn hình 2 dòng x 16 ký tự (tài nguyên dùng chung)
SemaphoreHandle_t mutexLcd;
bool dungMutex = false;

void lcdVietDong(int dong, const char* s) {           // ghi từng ký tự, mỗi ký tự mất 1 ms (giống LCD thật)
    for (int i = 0; i < 16; i++) {
        lcd[dong][i] = s[i] ? s[i] : ' ';
        vTaskDelay(1);                                // tạo cơ hội cho task khác chen vào
        if (!s[i]) { for (int k = i + 1; k < 16; k++) lcd[dong][k] = ' '; break; }
    }
}

void hienThi(const char* d0, const char* d1) {
    if (dungMutex) xSemaphoreTake(mutexLcd, portMAX_DELAY);   // vào vùng găng
    lcdVietDong(0, d0);
    lcdVietDong(1, d1);
    if (dungMutex) xSemaphoreGive(mutexLcd);                  // ra vùng găng – CHÍNH task đã take phải give
}

void taskNhietDo(void*) { for (;;) { hienThi("Nhiet do: 28.5C", "Do am   : 61%"); vTaskDelay(5); } }
void taskCanhBao(void*) { for (;;) { hienThi("!! CANH BAO !!", "Khoi vuot nguong"); vTaskDelay(7); } }

void chup(const char* tieuDe) {
    vTaskSuspendAll();                                // chụp nội dung LCD khi không ai đang ghi dở
    PRINT("%s\n  +----------------+\n  |%.16s|\n  |%.16s|\n  +----------------+", tieuDe, lcd[0], lcd[1]);
    xTaskResumeAll();
}

void taskKiemTra(void*) {
    vTaskDelay(pdMS_TO_TICKS(53));
    chup("KHÔNG có mutex – hai task ghi xen kẽ:");
    dungMutex = true;
    vTaskDelay(pdMS_TO_TICKS(200));
    xSemaphoreTake(mutexLcd, portMAX_DELAY);          // chờ tới lúc không ai đang ghi
    chup("CÓ mutex – mỗi lần chỉ một task ghi trọn vẹn:");
    xSemaphoreGive(mutexLcd);
    ket_thuc();
}

int main() {
    std::memset(lcd, ' ', sizeof(lcd));
    lcd[0][16] = lcd[1][16] = 0;
    mutexLcd = xSemaphoreCreateMutex();
    xTaskCreate(taskNhietDo, "NhietDo", 512, nullptr, 1, nullptr);
    xTaskCreate(taskCanhBao, "CanhBao", 512, nullptr, 1, nullptr);
    xTaskCreate(taskKiemTra, "KiemTra", 1024, nullptr, 2, nullptr);
    vTaskStartScheduler();
}
