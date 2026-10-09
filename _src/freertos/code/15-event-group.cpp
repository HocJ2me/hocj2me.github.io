// Bài 9 – Event group: chờ NHIỀU sự kiện (AND / OR) và đồng bộ nhiều task tại một điểm (rendezvous)
#include <initializer_list>
#include "sim.h"
#include "event_groups.h"

EventGroupHandle_t egKhoiDong, egDongBo;
constexpr EventBits_t BIT_WIFI = 1 << 0, BIT_SD = 1 << 1, BIT_CAM_BIEN = 1 << 2, BIT_LOI = 1 << 3;
constexpr EventBits_t TAT_CA = BIT_WIFI | BIT_SD | BIT_CAM_BIEN;

void taskKhoiTao(void* p) {
    auto bit = static_cast<EventBits_t>(reinterpret_cast<uintptr_t>(p));
    const char* ten = bit == BIT_WIFI ? "WiFi" : bit == BIT_SD ? "Thẻ SD" : "Cảm biến";
    uint32_t thoiGian = bit == BIT_WIFI ? 300 : bit == BIT_SD ? 120 : 200;
    vTaskDelay(pdMS_TO_TICKS(thoiGian));
    LOG("  %s sẵn sàng -> đặt bit 0x%lX", ten, (unsigned long)bit);
    xEventGroupSetBits(egKhoiDong, bit);
    vTaskDelete(nullptr);
}

void taskUngDung(void*) {
    LOG("UngDung  chờ TẤT CẢ: WiFi + SD + cảm biến (xWaitForAllBits = pdTRUE)");
    EventBits_t b = xEventGroupWaitBits(egKhoiDong, TAT_CA, pdFALSE, pdTRUE, portMAX_DELAY);
    LOG("UngDung  bits = 0x%lX -> hệ thống sẵn sàng, bắt đầu ghi log", (unsigned long)b);

    LOG("UngDung  chờ BẤT KỲ: lỗi hoặc ... (xWaitForAllBits = pdFALSE), tối đa 200 ms");
    b = xEventGroupWaitBits(egKhoiDong, BIT_LOI, pdTRUE, pdFALSE, pdMS_TO_TICKS(200));
    LOG("UngDung  hết giờ, bit lỗi = %s", (b & BIT_LOI) ? "CÓ" : "không");
    vTaskDelete(nullptr);
}

// ===== Rendezvous: 3 task (3 động cơ) phải cùng tới vạch xuất phát rồi mới chạy =====
constexpr EventBits_t DC1 = 1 << 0, DC2 = 1 << 1, DC3 = 1 << 2;
void taskDongCo(void* p) {
    int so = (int)reinterpret_cast<uintptr_t>(p);
    EventBits_t bitCuaToi = 1 << (so - 1);
    vTaskDelay(pdMS_TO_TICKS(800 + so * 70));                // mỗi động cơ hiệu chỉnh mất thời gian khác nhau
    LOG("  Động cơ %d hiệu chỉnh xong, chờ các động cơ khác", so);
    xEventGroupSync(egDongBo, bitCuaToi, DC1 | DC2 | DC3, portMAX_DELAY);
    LOG("  Động cơ %d XUẤT PHÁT", so);
    if (so == 3) { vTaskDelay(pdMS_TO_TICKS(10)); ket_thuc(); }
    vTaskDelete(nullptr);
}

int main() {
    egKhoiDong = xEventGroupCreate();
    egDongBo = xEventGroupCreate();
    xTaskCreate(taskUngDung, "UngDung", 512, nullptr, 3, nullptr);
    for (EventBits_t b : {BIT_WIFI, BIT_SD, BIT_CAM_BIEN})
        xTaskCreate(taskKhoiTao, "KhoiTao", 512, reinterpret_cast<void*>(uintptr_t(b)), 2, nullptr);
    for (int i = 1; i <= 3; i++) xTaskCreate(taskDongCo, "DongCo", 512, reinterpret_cast<void*>(uintptr_t(i)), 2, nullptr);
    vTaskStartScheduler();
}
