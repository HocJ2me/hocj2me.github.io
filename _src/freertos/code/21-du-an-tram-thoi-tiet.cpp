// Bài 12 – DỰ ÁN TỔNG HỢP: firmware trạm thời tiết đa nhiệm
//   TaskCamBien (ưu tiên 3, chu kỳ 200 ms, vTaskDelayUntil) --queue--> TaskXuLy (2)
//   TaskXuLy: lọc trung bình, cập nhật LCD (mutex), báo động qua event group
//   TaskCanhBao (4): chờ bit báo động           ISR nút nhấn --notification--> TaskGiaoDien (2): đổi chế độ hiển thị
//   Software timer 500 ms: nhịp tim (heartbeat LED)       Timer one-shot: kết thúc mô phỏng sau 2,5 giây
#include <cstdio>
#include "sim.h"
#include "queue.h"
#include "semphr.h"
#include "event_groups.h"
#include "timers.h"

struct MauDo { uint32_t thoiDiem; int16_t nhietX10; uint8_t doAm; };

QueueHandle_t qMau;
SemaphoreHandle_t mtxLcd;
EventGroupHandle_t egBaoDong;
TaskHandle_t hGiaoDien;
constexpr EventBits_t BIT_QUA_NHIET = 1 << 0;
volatile int cheDo = 0;                                   // 0: nhiệt độ, 1: độ ẩm
uint32_t soMau = 0, soLanCanhBao = 0;

void lcdIn(const char* s) {
    xSemaphoreTake(mtxLcd, portMAX_DELAY);
    LOG("    LCD | %-20s |", s);
    xSemaphoreGive(mtxLcd);
}

void taskCamBien(void*) {
    TickType_t moc = xTaskGetTickCount();
    const int16_t nhiet[] = {285, 287, 290, 295, 302, 311, 318, 322, 316, 305, 298, 291};
    for (int i = 0;; i = (i + 1) % 12) {
        MauDo m{xTaskGetTickCount(), nhiet[i], uint8_t(60 - i)};
        xQueueSend(qMau, &m, 0);
        vTaskDelayUntil(&moc, pdMS_TO_TICKS(200));
    }
}

void taskXuLy(void*) {
    int16_t lichSu[3] = {0};
    int dem = 0;
    MauDo m;
    for (;;) {
        xQueueReceive(qMau, &m, portMAX_DELAY);
        soMau++;
        lichSu[dem++ % 3] = m.nhietX10;
        int n = dem < 3 ? dem : 3, tong = 0;
        for (int i = 0; i < n; i++) tong += lichSu[i];
        int tb = tong / n;
        char s[32];
        if (cheDo == 0) std::snprintf(s, sizeof(s), "T = %d.%d C (TB3)", tb / 10, tb % 10);
        else            std::snprintf(s, sizeof(s), "H = %u %%", m.doAm);
        lcdIn(s);
        if (tb >= 310) xEventGroupSetBits(egBaoDong, BIT_QUA_NHIET);
        else           xEventGroupClearBits(egBaoDong, BIT_QUA_NHIET);
    }
}

void taskCanhBao(void*) {
    for (;;) {
        xEventGroupWaitBits(egBaoDong, BIT_QUA_NHIET, pdFALSE, pdTRUE, portMAX_DELAY);
        soLanCanhBao++;
        LOG("!! CanhBao  nhiệt độ TB >= 31.0 C -> bật còi, gửi SMS");
        vTaskDelay(pdMS_TO_TICKS(400));                     // nhắc lại mỗi 400 ms khi còn quá nhiệt
    }
}

uint32_t isrNutMode() {
    BaseType_t c = pdFALSE;
    vTaskNotifyGiveFromISR(hGiaoDien, &c);
    return c;
}

void taskGiaoDien(void*) {
    for (;;) {
        ulTaskNotifyTake(pdTRUE, portMAX_DELAY);
        cheDo = 1 - cheDo;
        LOG("GiaoDien  nút MODE -> hiển thị %s", cheDo ? "ĐỘ ẨM" : "NHIỆT ĐỘ");
    }
}

void cbNhipTim(TimerHandle_t) { static bool b; b = !b; LOG("  (heartbeat LED %s)", b ? "●" : "○"); }

void cbKetThuc(TimerHandle_t) {
    char bang[512];
    vTaskList(bang);
    PRINT("\n===== Tổng kết sau 2,5 giây =====\nSố mẫu đã xử lý: %lu, số lần cảnh báo: %lu\nTên            \tTT\tƯT\tStack\tSTT\n%s",
          (unsigned long)soMau, (unsigned long)soLanCanhBao, bang);
    ket_thuc();
}

void taskNguoiDung(void*) {                                   // giả lập nhấn nút MODE lúc 700 ms và 1300 ms
    vTaskDelay(pdMS_TO_TICKS(700));  phatNgat(3);
    vTaskDelay(pdMS_TO_TICKS(600));  phatNgat(3);
    vTaskDelete(nullptr);
}

int main() {
    qMau = xQueueCreate(8, sizeof(MauDo));
    mtxLcd = xSemaphoreCreateMutex();
    egBaoDong = xEventGroupCreate();
    dangKyNgat(3, isrNutMode);
    xTaskCreate(taskCamBien,   "CamBien",   512,  nullptr, 3, nullptr);
    xTaskCreate(taskXuLy,      "XuLy",      1024, nullptr, 2, nullptr);
    xTaskCreate(taskCanhBao,   "CanhBao",   512,  nullptr, 4, nullptr);
    xTaskCreate(taskGiaoDien,  "GiaoDien",  512,  nullptr, 2, &hGiaoDien);
    xTaskCreate(taskNguoiDung, "NguoiDung", 512,  nullptr, 1, nullptr);
    xTimerStart(xTimerCreate("NhipTim", pdMS_TO_TICKS(500), pdTRUE, nullptr, cbNhipTim), 0);
    xTimerStart(xTimerCreate("KetThuc", pdMS_TO_TICKS(2500), pdFALSE, nullptr, cbKetThuc), 0);
    vTaskStartScheduler();
}
