// Bài 11: Checksum và CRC-8 – kiểm tra lỗi khi truyền dữ liệu qua UART/I2C/LoRa
#include <cstdint>
#include <cstdio>

uint8_t checksumXor(const uint8_t* d, size_t n) {
    uint8_t c = 0;
    for (size_t i = 0; i < n; i++) c ^= d[i];
    return c;
}

// CRC-8 đa thức 0x31 (dùng trong cảm biến Sensirion SHT3x, khởi tạo 0xFF)
uint8_t crc8(const uint8_t* d, size_t n) {
    uint8_t crc = 0xFF;
    for (size_t i = 0; i < n; i++) {
        crc ^= d[i];
        for (int b = 0; b < 8; b++) crc = (crc & 0x80) ? (crc << 1) ^ 0x31 : (crc << 1);
    }
    return crc;
}

int main() {
    uint8_t goi[] = {0xBE, 0xEF};
    std::printf("Dữ liệu BE EF: XOR = 0x%02X, CRC-8 = 0x%02X (datasheet SHT3x ghi 0x92)\n",
                checksumXor(goi, 2), crc8(goi, 2));

    uint8_t gui[] = {0x01, 0x1D, 0x01, 0x41};
    uint8_t crcGui = crc8(gui, 4);
    uint8_t nhan[] = {0x01, 0x1D, 0x03, 0x41};             // 1 bit bị nhiễu trên đường truyền
    std::printf("Gói gửi CRC = 0x%02X, gói nhận CRC = 0x%02X -> %s\n", crcGui, crc8(nhan, 4),
                crcGui == crc8(nhan, 4) ? "OK" : "PHÁT HIỆN LỖI, yêu cầu gửi lại");
}
