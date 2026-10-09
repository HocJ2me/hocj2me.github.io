// sim.h – tiện ích cho các ví dụ chạy trên bản mô phỏng FreeRTOS (Windows).
// Trên board thật: thay LOG(...) bằng Serial.printf(...) (Arduino-ESP32) hoặc ESP_LOGI(TAG, ...) (ESP-IDF),
// bỏ ket_thuc() vì firmware không bao giờ kết thúc.
#pragma once
#include <cstdio>
#include <cstdlib>
#include "FreeRTOS.h"
#include "task.h"

// In một dòng kèm mốc thời gian (ms tính từ lúc scheduler chạy).
// Đặt trong critical section để hai task không in chen nhau.
#define LOG(fmt, ...)                                                                     \
    do {                                                                                  \
        taskENTER_CRITICAL();                                                             \
        std::printf("[%5lu ms] " fmt "\n", (unsigned long)xTaskGetTickCount(), ##__VA_ARGS__); \
        std::fflush(stdout);                                                              \
        taskEXIT_CRITICAL();                                                              \
    } while (0)

// In không kèm thời gian (dùng trước khi scheduler chạy hoặc để in bảng)
#define PRINT(fmt, ...) do { std::printf(fmt "\n", ##__VA_ARGS__); std::fflush(stdout); } while (0)

// ===== Giả lập NGẮT phần cứng (chỉ có trên bản mô phỏng) =====
// Trên ESP32: attachInterrupt(pin, isr, FALLING) hoặc gpio_isr_handler_add(...)
// Trên STM32: hàm HAL_GPIO_EXTI_Callback(...) được gọi trong ngắt EXTI
// Hàm ISR mô phỏng phải trả về pdTRUE nếu cần chuyển ngữ cảnh ngay sau ngắt.
inline void dangKyNgat(uint32_t soNgat, uint32_t (*isr)(void)) { vPortSetInterruptHandler(soNgat, isr); }
inline void phatNgat(uint32_t soNgat) { vPortGenerateSimulatedInterrupt(soNgat); }   // "phần cứng" bật cờ ngắt

// Bận tính toán đúng n ms (giả lập công việc nặng, KHÔNG nhường CPU như vTaskDelay)
inline void banTinhToan(uint32_t ms) {
    for (uint32_t i = 0; i < ms; i++) {
        TickType_t t = xTaskGetTickCount();
        while (xTaskGetTickCount() == t) { }
    }
}

// Kết thúc chương trình mô phỏng (chỉ dùng trên máy tính)
inline void ket_thuc() {
    std::fflush(stdout);
    std::exit(0);
}
