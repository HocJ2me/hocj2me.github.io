// Bài 10 – Message buffer: gửi các THÔNG ĐIỆP có độ dài thay đổi; bên nhận luôn nhận trọn từng thông điệp.
// Đây cũng là cơ chế FreeRTOS gợi ý để trao đổi dữ liệu giữa 2 nhân (core-to-core) trên chip đa nhân.
#include <cstring>
#include "sim.h"
#include "message_buffer.h"

MessageBufferHandle_t mbLenh;

void taskBluetooth(void*) {                             // "nhân 0": nhận lệnh từ điện thoại
    const char* lenh[] = {"LED ON", "SERVO 90", "PLAY_MELODY twinkle_twinkle_little_star", "STOP"};
    for (const char* l : lenh) {
        size_t n = xMessageBufferSend(mbLenh, l, std::strlen(l), portMAX_DELAY);
        LOG("Bluetooth gửi thông điệp %2u byte: \"%s\"", (unsigned)n, l);
        vTaskDelay(pdMS_TO_TICKS(30));
    }
    vTaskDelete(nullptr);
}

void taskThucThi(void*) {                               // "nhân 1": thực thi lệnh
    vTaskDelay(pdMS_TO_TICKS(100));                     // bận lúc đầu -> các thông điệp dồn lại
    LOG("ThucThi  còn trống %u byte trong buffer", (unsigned)xMessageBufferSpacesAvailable(mbLenh));
    char buf[64];
    size_t n;
    while ((n = xMessageBufferReceive(mbLenh, buf, sizeof(buf) - 1, pdMS_TO_TICKS(200))) > 0) {
        buf[n] = 0;
        LOG("ThucThi  nhận nguyên vẹn %2u byte: \"%s\"", (unsigned)n, buf);
    }
    LOG("ThucThi  hết thông điệp (mỗi thông điệp tốn thêm %u byte lưu độ dài)", (unsigned)sizeof(size_t));
    ket_thuc();
}

int main() {
    mbLenh = xMessageBufferCreate(200);
    xTaskCreate(taskBluetooth, "Bluetooth", 512, nullptr, 2, nullptr);
    xTaskCreate(taskThucThi,   "ThucThi",   1024, nullptr, 1, nullptr);
    vTaskStartScheduler();
}
