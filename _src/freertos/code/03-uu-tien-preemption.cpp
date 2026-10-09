// Bài 3 – Ưu tiên và chiếm quyền (preemption): task ưu tiên cao chen ngang ngay khi sẵn sàng.
// Phần 2: task ưu tiên cao KHÔNG nhường CPU -> task thấp bị "đói" (starvation).
#include "sim.h"

void taskNen(void*) {                        // ưu tiên 1: việc nền nặng
    for (int i = 1; i <= 10; i++) {
        banTinhToan(100);                    // tính toán liên tục 100 ms, không nhường CPU
        LOG("  Nen      xong khối việc %d", i);
    }
    vTaskDelete(nullptr);
}

void taskKhanCap(void*) {                    // ưu tiên 3: phải phản hồi đúng hạn
    TickType_t moc = xTaskGetTickCount();
    for (int i = 0; i < 3; i++) {
        vTaskDelayUntil(&moc, pdMS_TO_TICKS(170));
        LOG("KhanCap  đọc cảm biến khí gas (chen ngang task nền)");
    }
    vTaskDelete(nullptr);
}

void taskThamLam(void*) {                    // ưu tiên 2: chạy liên tục 300 ms không nghỉ
    vTaskDelay(pdMS_TO_TICKS(700));
    LOG("ThamLam  bắt đầu chiếm CPU 300 ms (không gọi vTaskDelay)");
    banTinhToan(300);
    LOG("ThamLam  xong – trong 300 ms đó task Nen (ưu tiên 1) không chạy được");
    vTaskDelay(pdMS_TO_TICKS(350));
    ket_thuc();
}

int main() {
    xTaskCreate(taskNen,     "Nen",     512, nullptr, 1, nullptr);
    xTaskCreate(taskKhanCap, "KhanCap", 512, nullptr, 3, nullptr);
    xTaskCreate(taskThamLam, "ThamLam", 512, nullptr, 2, nullptr);
    vTaskStartScheduler();
}
