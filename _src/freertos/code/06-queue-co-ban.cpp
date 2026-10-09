// Bài 5 – Queue cơ bản: task sản xuất gửi dữ liệu, task tiêu thụ chờ (bị chặn) cho tới khi có dữ liệu.
// Phần 2: hàng đợi đầy khi bên gửi nhanh hơn bên nhận.
#include "sim.h"
#include "queue.h"

QueueHandle_t qNhietDo;

void taskDocCamBien(void*) {                          // producer
    for (int i = 0; i < 4; i++) {
        int t = 280 + i * 3;                          // nhiệt độ x10
        LOG("DocCamBien gửi %d", t);
        xQueueSend(qNhietDo, &t, portMAX_DELAY);      // sao chép giá trị vào hàng đợi
        vTaskDelay(pdMS_TO_TICKS(200));
    }
    vTaskDelete(nullptr);
}

void taskHienThi(void*) {                             // consumer
    int t;
    for (int i = 0; i < 4; i++) {
        xQueueReceive(qNhietDo, &t, portMAX_DELAY);   // ngủ (Blocked) tới khi có dữ liệu – không tốn CPU
        LOG("  HienThi  nhận %d -> LCD: %d.%d°C", t, t / 10, t % 10);
    }
    vTaskDelete(nullptr);
}

QueueHandle_t qNho;
void taskGuiNhanh(void*) {
    vTaskDelay(pdMS_TO_TICKS(1000));
    LOG("== Phần 2: hàng đợi 3 phần tử, gửi mỗi 50 ms, nhận mỗi 200 ms ==");
    for (int i = 1; i <= 8; i++) {
        BaseType_t ok = xQueueSend(qNho, &i, 0);      // timeout 0: không chờ nếu đầy
        LOG("GuiNhanh  gửi %d -> %s (đang chờ %u)", i, ok == pdPASS ? "OK" : "ĐẦY, bỏ mất", (unsigned)uxQueueMessagesWaiting(qNho));
        vTaskDelay(pdMS_TO_TICKS(50));
    }
    vTaskDelete(nullptr);
}

void taskNhanCham(void*) {
    vTaskDelay(pdMS_TO_TICKS(1000));
    int v;
    while (xQueueReceive(qNho, &v, pdMS_TO_TICKS(500)) == pdPASS) {   // chờ tối đa 500 ms
        LOG("  NhanCham nhận %d", v);
        vTaskDelay(pdMS_TO_TICKS(200));
    }
    LOG("  NhanCham hết 500 ms không có dữ liệu -> kết thúc");
    ket_thuc();
}

int main() {
    qNhietDo = xQueueCreate(5, sizeof(int));          // 5 phần tử, mỗi phần tử sizeof(int) byte
    qNho = xQueueCreate(3, sizeof(int));
    xTaskCreate(taskDocCamBien, "DocCamBien", 512, nullptr, 2, nullptr);
    xTaskCreate(taskHienThi,    "HienThi",    512, nullptr, 1, nullptr);
    xTaskCreate(taskGuiNhanh,   "GuiNhanh",   512, nullptr, 2, nullptr);
    xTaskCreate(taskNhanCham,   "NhanCham",   512, nullptr, 1, nullptr);
    vTaskStartScheduler();
}
