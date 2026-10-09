// Bài 4 – Idle task, idle hook (đo tải CPU), vùng găng, tạm dừng scheduler, liệt kê task
#include "sim.h"

volatile uint32_t demIdle = 0;

// Idle hook: được gọi liên tục khi KHÔNG có task nào khác sẵn sàng.
// Không được chặn (không vTaskDelay). Thường dùng để: đo CPU rảnh, cho chip vào chế độ ngủ.
extern "C" void vApplicationIdleHook(void) {
    static TickType_t lanCuoi = 0;
    TickType_t now = xTaskGetTickCount();
    if (now != lanCuoi) { lanCuoi = now; demIdle++; }   // đếm số tick CPU rảnh
}

void taskBan(void*) {
    for (int i = 0; i < 3; i++) {
        banTinhToan(60);                 // bận 60 ms
        vTaskDelay(pdMS_TO_TICKS(140));  // nghỉ 140 ms -> tải CPU ~30%
    }
    vTaskDelete(nullptr);
}

volatile int biengChung = 0;
void taskBaoCao(void*) {
    vTaskDelay(pdMS_TO_TICKS(20));
    char bang[512];
    vTaskList(bang);                     // bảng: Tên  Trạng thái  Ưu tiên  Stack trống  Số thứ tự
    PRINT("Tên            \tTT\tƯT\tStack\tSTT\n%s", bang);
    PRINT("(TT: X=đang chạy, R=sẵn sàng, B=bị chặn, S=tạm dừng, D=đã xoá)\n");

    // Vùng găng (critical section): tắt ngắt/không chuyển task – phải thật NGẮN
    taskENTER_CRITICAL();
    biengChung++;
    taskEXIT_CRITICAL();

    // Tạm dừng scheduler: các task khác không chạy nhưng ngắt vẫn hoạt động
    vTaskSuspendAll();
    biengChung++;
    xTaskResumeAll();
    LOG("BaoCao   biengChung = %d (sửa an toàn 2 lần)", biengChung);

    TickType_t batDau = xTaskGetTickCount();
    uint32_t idleBatDau = demIdle;
    vTaskDelay(pdMS_TO_TICKS(600));
    uint32_t tong = xTaskGetTickCount() - batDau, ranh = demIdle - idleBatDau;
    LOG("BaoCao   trong %lu ms: CPU rảnh ~%lu ms -> tải CPU ~%lu%%", (unsigned long)tong, (unsigned long)ranh,
        (unsigned long)(100 - ranh * 100 / tong));
    LOG("BaoCao   tên task hiện tại: %s, idle task: %s", pcTaskGetName(nullptr), pcTaskGetName(xTaskGetIdleTaskHandle()));
    ket_thuc();
}

int main() {
    xTaskCreate(taskBan,     "Ban",     512,  nullptr, 1, nullptr);
    xTaskCreate(taskBaoCao,  "BaoCao",  2048, nullptr, 2, nullptr);
    vTaskStartScheduler();
}
