// Bài 7 – Mutex đệ quy (recursive mutex): một task lấy CÙNG một khoá nhiều lần (hàm gọi lồng nhau).
// Với mutex thường, lần lấy thứ hai sẽ tự khoá chính mình (deadlock).
#include "sim.h"
#include "semphr.h"

SemaphoreHandle_t mutexThuong, mutexDeQuy;

void ghiByte(uint8_t b) {                            // hàm cấp thấp: tự khoá bus I2C
    xSemaphoreTakeRecursive(mutexDeQuy, portMAX_DELAY);
    LOG("    ghiByte(0x%02X) – đang giữ khoá", b);
    xSemaphoreGiveRecursive(mutexDeQuy);
}

void ghiGoiTin(const uint8_t* d, int n) {            // hàm cấp cao: khoá cả gói, rồi gọi hàm cấp thấp (cũng khoá)
    xSemaphoreTakeRecursive(mutexDeQuy, portMAX_DELAY);
    LOG("  ghiGoiTin: lấy khoá lần 1");
    for (int i = 0; i < n; i++) ghiByte(d[i]);       // lấy khoá lần 2, 3, ... trong cùng task – hợp lệ
    xSemaphoreGiveRecursive(mutexDeQuy);             // số lần give phải bằng số lần take
    LOG("  ghiGoiTin: trả khoá – task khác giờ mới lấy được");
}

void taskChinh(void*) {
    LOG("== Recursive mutex ==");
    const uint8_t goi[] = {0x3C, 0xA5, 0x01};
    ghiGoiTin(goi, 3);

    LOG("== Mutex thường bị lấy 2 lần trong cùng task ==");
    xSemaphoreTake(mutexThuong, portMAX_DELAY);
    LOG("  lấy lần 1: OK");
    BaseType_t ok = xSemaphoreTake(mutexThuong, pdMS_TO_TICKS(200));   // chờ chính mình -> không bao giờ được
    LOG("  lấy lần 2 (chờ tối đa 200 ms): %s", ok ? "OK" : "THẤT BẠI – nếu chờ portMAX_DELAY sẽ treo vĩnh viễn (deadlock)");
    xSemaphoreGive(mutexThuong);
    ket_thuc();
}

int main() {
    mutexThuong = xSemaphoreCreateMutex();
    mutexDeQuy = xSemaphoreCreateRecursiveMutex();
    xTaskCreate(taskChinh, "Chinh", 1024, nullptr, 1, nullptr);
    vTaskStartScheduler();
}
