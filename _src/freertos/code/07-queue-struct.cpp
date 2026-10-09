// Bài 5 – Queue chứa struct: nhiều task nguồn gửi về một task ghi log; tin khẩn gửi lên ĐẦU hàng đợi;
// xQueuePeek xem mà không lấy; gửi từ ngắt bằng xQueueSendFromISR.
#include "sim.h"
#include "queue.h"

enum Nguon : uint8_t { NHIET, DO_AM, KHOI, NUT };
const char* TEN_NGUON[] = {"Nhiệt độ", "Độ ẩm", "Khói", "Nút nhấn"};

struct BanTin {
    Nguon nguon;
    int16_t giaTri;
    bool khanCap;
};

QueueHandle_t qLog;

void taskNhiet(void*) {
    for (int i = 0; i < 3; i++) {
        BanTin b{NHIET, int16_t(28 + i), false};
        xQueueSend(qLog, &b, portMAX_DELAY);
        vTaskDelay(pdMS_TO_TICKS(150));
    }
    vTaskDelete(nullptr);
}

void taskDoAm(void*) {
    for (int i = 0; i < 3; i++) {
        BanTin b{DO_AM, int16_t(60 - i), false};
        xQueueSend(qLog, &b, portMAX_DELAY);
        vTaskDelay(pdMS_TO_TICKS(150));
    }
    vTaskDelete(nullptr);
}

void taskKhoi(void*) {
    vTaskDelay(pdMS_TO_TICKS(140));
    BanTin b{KHOI, 850, true};
    xQueueSendToFront(qLog, &b, portMAX_DELAY);     // chen lên ĐẦU hàng đợi
    vTaskDelete(nullptr);
}

// ISR nút nhấn: dùng phiên bản ...FromISR, không bao giờ chờ
uint32_t isrNut() {
    BaseType_t canChuyen = pdFALSE;
    BanTin b{NUT, 1, false};
    xQueueSendFromISR(qLog, &b, &canChuyen);
    return canChuyen;                                // pdTRUE nếu task đang chờ có ưu tiên cao hơn task bị ngắt
}

void taskPhanCung(void*) {                           // giả lập: người dùng nhấn nút lúc 300 ms
    vTaskDelay(pdMS_TO_TICKS(300));
    phatNgat(3);
    vTaskDelete(nullptr);
}

void taskGhiLog(void*) {
    vTaskDelay(pdMS_TO_TICKS(100));                  // ghi log chậm: để bản tin dồn lại trong hàng đợi
    BanTin b;
    while (xQueuePeek(qLog, &b, pdMS_TO_TICKS(400)) == pdPASS) {
        if (b.khanCap) LOG("GhiLog   (peek) thấy tin khẩn ở đầu hàng đợi!");
        xQueueReceive(qLog, &b, 0);
        LOG("GhiLog   %s = %d%s", TEN_NGUON[b.nguon], b.giaTri, b.khanCap ? "   <<< KHẨN" : "");
        vTaskDelay(pdMS_TO_TICKS(40));
    }
    LOG("GhiLog   hàng đợi trống, kết thúc. sizeof(BanTin) = %u byte", (unsigned)sizeof(BanTin));
    ket_thuc();
}

int main() {
    qLog = xQueueCreate(10, sizeof(BanTin));
    dangKyNgat(3, isrNut);
    xTaskCreate(taskNhiet,    "Nhiet",    512, nullptr, 2, nullptr);
    xTaskCreate(taskDoAm,     "DoAm",     512, nullptr, 2, nullptr);
    xTaskCreate(taskKhoi,     "Khoi",     512, nullptr, 3, nullptr);
    xTaskCreate(taskPhanCung, "PhanCung", 512, nullptr, 4, nullptr);
    xTaskCreate(taskGhiLog,   "GhiLog",   1024, nullptr, 1, nullptr);
    vTaskStartScheduler();
}
