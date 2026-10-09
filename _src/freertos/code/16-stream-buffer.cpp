// Bài 10 – Stream buffer: chuyển luồng BYTE từ ngắt (UART nhận dữ liệu GPS) sang task.
// Một bên ghi – một bên đọc, không cần mutex. Task được đánh thức khi đủ "trigger level" byte.
#include <cstring>
#include "sim.h"
#include "stream_buffer.h"

StreamBufferHandle_t sbUart;
const char DU_LIEU_GPS[] = "$GPGGA,21.0285N,105.8542E*4A\n$GPGGA,21.0290N,105.8551E*47\n";
volatile size_t viTriPhat = 0;

uint32_t isrUartRx() {                                 // mỗi ngắt "nhận" 4 byte từ module GPS
    BaseType_t c = pdFALSE;
    size_t con = std::strlen(DU_LIEU_GPS) - viTriPhat;
    size_t n = con < 4 ? con : 4;
    xStreamBufferSendFromISR(sbUart, DU_LIEU_GPS + viTriPhat, n, &c);
    viTriPhat += n;
    return c;
}

void taskPhanCung(void*) {                             // UART tạo ngắt mỗi 10 ms
    while (viTriPhat < std::strlen(DU_LIEU_GPS)) {
        phatNgat(3);
        vTaskDelay(pdMS_TO_TICKS(10));
    }
    vTaskDelete(nullptr);
}

void taskDocGps(void*) {
    char dong[64];
    size_t len = 0;
    for (;;) {
        char buf[16];
        size_t n = xStreamBufferReceive(sbUart, buf, sizeof(buf), pdMS_TO_TICKS(200));  // nhận tối đa 16 byte
        if (n == 0) { LOG("DocGps  không còn dữ liệu"); ket_thuc(); }
        LOG("DocGps  nhận khối %2u byte", (unsigned)n);
        for (size_t i = 0; i < n; i++) {
            if (buf[i] == '\n') { dong[len] = 0; LOG("DocGps  >>> câu NMEA hoàn chỉnh: %s", dong); len = 0; }
            else if (len < sizeof(dong) - 1) dong[len++] = buf[i];
        }
    }
}

int main() {
    sbUart = xStreamBufferCreate(128, 12);              // dung lượng 128 byte, đánh thức task khi có >= 12 byte
    dangKyNgat(3, isrUartRx);
    xTaskCreate(taskDocGps,   "DocGps",   1024, nullptr, 2, nullptr);
    xTaskCreate(taskPhanCung, "PhanCung", 512,  nullptr, 3, nullptr);
    vTaskStartScheduler();
}
