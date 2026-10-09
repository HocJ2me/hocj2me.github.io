// Bài 11 – Software timer: one-shot và auto-reload, timer ID, đổi chu kỳ, dừng timer.
// Callback chạy trong task "Tmr Svc" (timer daemon) – KHÔNG được chặn (không vTaskDelay, không chờ lâu).
#include "sim.h"
#include "timers.h"

TimerHandle_t tmrNhay, tmrTatBom, tmrDemNguoc;

void cbNhayLed(TimerHandle_t t) {                       // auto-reload: gọi lặp lại
    static bool led = false;
    led = !led;
    LOG("  [timer NhayLed] LED %s (chạy trong task: %s)", led ? "BẬT" : "TẮT", pcTaskGetName(nullptr));
    (void)t;
}

void cbTatBom(TimerHandle_t) {                          // one-shot: chỉ gọi một lần
    LOG("  [timer TatBom] ĐÃ TƯỚI ĐỦ 500 ms -> tắt bơm");
}

void cbDemNguoc(TimerHandle_t t) {                      // dùng timer ID để lưu bộ đếm riêng của timer
    uintptr_t con = reinterpret_cast<uintptr_t>(pvTimerGetTimerID(t));
    LOG("  [timer DemNguoc] còn %u", (unsigned)con);
    if (con == 0) { xTimerStop(t, 0); LOG("  [timer DemNguoc] dừng timer"); return; }
    vTimerSetTimerID(t, reinterpret_cast<void*>(con - 1));
}

void taskChinh(void*) {
    LOG("Chinh  bật bơm, khởi động các timer");
    xTimerStart(tmrNhay, 0);
    xTimerStart(tmrTatBom, 0);
    vTaskDelay(pdMS_TO_TICKS(700));
    LOG("Chinh  đổi chu kỳ nháy LED 200 ms -> 80 ms");
    xTimerChangePeriod(tmrNhay, pdMS_TO_TICKS(80), 0);
    vTaskDelay(pdMS_TO_TICKS(300));
    xTimerStop(tmrNhay, 0);
    LOG("Chinh  dừng timer nháy; timer TatBom còn hoạt động? %s", xTimerIsTimerActive(tmrTatBom) ? "có" : "không");
    xTimerStart(tmrDemNguoc, 0);
    vTaskDelay(pdMS_TO_TICKS(450));
    ket_thuc();
}

int main() {
    // xTimerCreate(tên, chu kỳ, auto-reload?, ID, callback)
    tmrNhay     = xTimerCreate("NhayLed",  pdMS_TO_TICKS(200), pdTRUE,  nullptr, cbNhayLed);
    tmrTatBom   = xTimerCreate("TatBom",   pdMS_TO_TICKS(500), pdFALSE, nullptr, cbTatBom);
    tmrDemNguoc = xTimerCreate("DemNguoc", pdMS_TO_TICKS(100), pdTRUE,  reinterpret_cast<void*>(3), cbDemNguoc);
    xTaskCreate(taskChinh, "Chinh", 1024, nullptr, 1, nullptr);
    vTaskStartScheduler();
}
