// Bài 2 – Task: một hàm dùng cho nhiều task (tham số khác nhau), task tạo tĩnh, handle, trạng thái, stack
#include "sim.h"

struct CauHinhCamBien {
    const char* ten;
    int chuKyMs;
    int giaTriGoc;
};

void taskCamBien(void* p) {
    const CauHinhCamBien* cfg = static_cast<const CauHinhCamBien*>(p);
    for (int i = 0; i < 3; i++) {
        LOG("%-8s đọc được %d", cfg->ten, cfg->giaTriGoc + i);
        vTaskDelay(pdMS_TO_TICKS(cfg->chuKyMs));
    }
    LOG("%-8s xong, stack còn trống ít nhất %u word", cfg->ten, (unsigned)uxTaskGetStackHighWaterMark(nullptr));
    vTaskDelete(nullptr);
}

// ===== Task tạo TĨNH: bộ nhớ stack và TCB do ta cấp, không dùng heap =====
StackType_t stackTinh[256];
StaticTask_t tcbTinh;
void taskBaoThuc(void*) {
    for (;;) {
        LOG("BaoThuc  bíp! (task tĩnh)");
        vTaskDelay(pdMS_TO_TICKS(400));
    }
}

const char* tenTrangThai(eTaskState s) {
    switch (s) {
        case eRunning:   return "Running";
        case eReady:     return "Ready";
        case eBlocked:   return "Blocked";
        case eSuspended: return "Suspended";
        case eDeleted:   return "Deleted";
        default:         return "?";
    }
}

TaskHandle_t hBaoThuc = nullptr;

void taskQuanLy(void*) {
    vTaskDelay(pdMS_TO_TICKS(50));
    LOG("QuanLy   trạng thái BaoThuc: %s", tenTrangThai(eTaskGetState(hBaoThuc)));
    vTaskDelay(pdMS_TO_TICKS(900));
    LOG("QuanLy   số task đang tồn tại: %u", (unsigned)uxTaskGetNumberOfTasks());
    LOG("QuanLy   xoá task BaoThuc");
    vTaskDelete(hBaoThuc);
    vTaskDelay(pdMS_TO_TICKS(500));
    LOG("QuanLy   số task còn lại: %u (gồm IDLE và Tmr Svc)", (unsigned)uxTaskGetNumberOfTasks());
    ket_thuc();
}

int main() {
    static const CauHinhCamBien nhiet{"Nhiet", 300, 28};
    static const CauHinhCamBien doAm{"DoAm", 450, 60};
    xTaskCreate(taskCamBien, "Nhiet", 512, (void*)&nhiet, 1, nullptr);   // cùng hàm,
    xTaskCreate(taskCamBien, "DoAm",  512, (void*)&doAm,  1, nullptr);   // khác tham số
    hBaoThuc = xTaskCreateStatic(taskBaoThuc, "BaoThuc", 256, nullptr, 1, stackTinh, &tcbTinh);
    xTaskCreate(taskQuanLy, "QuanLy", 512, nullptr, 2, nullptr);
    vTaskStartScheduler();
}
