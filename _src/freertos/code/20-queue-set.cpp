// Bài 12 – Queue set: một task chờ đồng thời trên NHIỀU queue/semaphore, xử lý cái nào có dữ liệu trước.
#include <initializer_list>
#include "sim.h"
#include "queue.h"
#include "semphr.h"

QueueHandle_t qNhiet, qLenh;
SemaphoreHandle_t semKhanCap;
QueueSetHandle_t tapHop;

void taskNguonNhiet(void*) {
    for (int t : {280, 285, 291}) { xQueueSend(qNhiet, &t, 0); vTaskDelay(pdMS_TO_TICKS(120)); }
    vTaskDelete(nullptr);
}
void taskNguonLenh(void*) {
    vTaskDelay(pdMS_TO_TICKS(60));
    char c = 'F'; xQueueSend(qLenh, &c, 0);
    vTaskDelay(pdMS_TO_TICKS(150));
    c = 'S'; xQueueSend(qLenh, &c, 0);
    vTaskDelay(pdMS_TO_TICKS(50));
    xSemaphoreGive(semKhanCap);
    vTaskDelete(nullptr);
}

void taskXuLy(void*) {
    for (;;) {
        QueueSetMemberHandle_t ai = xQueueSelectFromSet(tapHop, pdMS_TO_TICKS(300));   // chờ BẤT KỲ thành viên nào
        if (ai == qNhiet) {
            int t; xQueueReceive(qNhiet, &t, 0);
            LOG("XuLy  từ qNhiet: %d.%d°C", t / 10, t % 10);
        } else if (ai == qLenh) {
            char c; xQueueReceive(qLenh, &c, 0);
            LOG("XuLy  từ qLenh : lệnh '%c'", c);
        } else if (ai == semKhanCap) {
            xSemaphoreTake(semKhanCap, 0);
            LOG("XuLy  từ semKhanCap: DỪNG KHẨN CẤP");
        } else {
            LOG("XuLy  300 ms không có gì -> kết thúc");
            ket_thuc();
        }
    }
}

int main() {
    qNhiet = xQueueCreate(4, sizeof(int));
    qLenh = xQueueCreate(4, sizeof(char));
    semKhanCap = xSemaphoreCreateBinary();
    tapHop = xQueueCreateSet(4 + 4 + 1);                 // tổng sức chứa của các thành viên
    xQueueAddToSet(qNhiet, tapHop);
    xQueueAddToSet(qLenh, tapHop);
    xQueueAddToSet(semKhanCap, tapHop);
    xTaskCreate(taskXuLy,       "XuLy",       1024, nullptr, 3, nullptr);
    xTaskCreate(taskNguonNhiet, "NguonNhiet", 512,  nullptr, 2, nullptr);
    xTaskCreate(taskNguonLenh,  "NguonLenh",  512,  nullptr, 2, nullptr);
    vTaskStartScheduler();
}
