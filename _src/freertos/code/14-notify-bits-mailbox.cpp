// Bài 8 – Task notification dùng như EVENT GROUP (từng bit là một sự kiện) và như MAILBOX (ghi đè giá trị mới nhất)
#include "sim.h"

constexpr uint32_t BIT_WIFI = 1u << 0, BIT_NUT = 1u << 1, BIT_PIN_YEU = 1u << 2;
TaskHandle_t hQuanLy = nullptr, hHienThi = nullptr;

void taskQuanLy(void*) {
    for (int i = 0; i < 3; i++) {
        uint32_t bits = 0;
        // Chờ bất kỳ bit nào; khi thoát xoá hết các bit (0xFFFFFFFF)
        xTaskNotifyWait(0, 0xFFFFFFFF, &bits, portMAX_DELAY);
        LOG("QuanLy   nhận bits = 0x%lX:%s%s%s", (unsigned long)bits,
            (bits & BIT_WIFI) ? " [WiFi đã kết nối]" : "", (bits & BIT_NUT) ? " [Nút nhấn]" : "",
            (bits & BIT_PIN_YEU) ? " [Pin yếu]" : "");
    }
    vTaskDelete(nullptr);
}

void taskWifi(void*) { vTaskDelay(pdMS_TO_TICKS(100)); xTaskNotify(hQuanLy, BIT_WIFI, eSetBits); vTaskDelete(nullptr); }
void taskNut(void*)  {
    vTaskDelay(pdMS_TO_TICKS(250));
    xTaskNotify(hQuanLy, BIT_NUT, eSetBits);
    xTaskNotify(hQuanLy, BIT_PIN_YEU, eSetBits);          // hai sự kiện gần như cùng lúc -> gộp trong một lần nhận
    vTaskDelay(pdMS_TO_TICKS(100));
    xTaskNotify(hQuanLy, BIT_NUT, eSetBits);
    vTaskDelete(nullptr);
}

// ===== Mailbox: chỉ cần giá trị MỚI NHẤT, giá trị cũ chưa đọc thì ghi đè =====
void taskCamBien(void*) {
    vTaskDelay(pdMS_TO_TICKS(500));
    for (int t = 280; t <= 300; t += 4) {
        xTaskNotify(hHienThi, t, eSetValueWithOverwrite);
        LOG("CamBien  ghi %d vào mailbox", t);
        vTaskDelay(pdMS_TO_TICKS(50));
    }
    vTaskDelete(nullptr);
}

void taskHienThi(void*) {
    vTaskDelay(pdMS_TO_TICKS(500));
    for (int i = 0; i < 3; i++) {
        uint32_t v;
        xTaskNotifyWait(0, 0, &v, portMAX_DELAY);
        LOG("  HienThi  LCD cập nhật chậm (120 ms/lần), đọc giá trị mới nhất: %lu", (unsigned long)v);
        vTaskDelay(pdMS_TO_TICKS(120));
    }
    ket_thuc();
}

int main() {
    xTaskCreate(taskQuanLy,  "QuanLy",  512, nullptr, 3, &hQuanLy);
    xTaskCreate(taskWifi,    "Wifi",    512, nullptr, 2, nullptr);
    xTaskCreate(taskNut,     "Nut",     512, nullptr, 4, nullptr);   // ưu tiên cao hơn QuanLy: gửi xong cả 2 bit rồi QuanLy mới chạy
    xTaskCreate(taskHienThi, "HienThi", 512, nullptr, 1, &hHienThi);
    xTaskCreate(taskCamBien, "CamBien", 512, nullptr, 2, nullptr);
    vTaskStartScheduler();
}
