// Chương trình chính của bộ mô phỏng: nạp kịch bản, gọi setup() một lần rồi loop() liên tục tới hết thời gian.
#include "Arduino.h"

void setup();
void loop();
void sim_kich_ban();

int main() {
    std::setvbuf(stdout, nullptr, _IOFBF, 1 << 16);
    sim_kich_ban();
    setup();
    while (sim::ms() < sim::end_ms) {
        loop();
        sim::advance_us(sim::loop_us);
    }
    if (sim::serial_open_line) std::printf("\n");
    sim::flush_pending();
    std::printf("── hết mô phỏng tại %u ms ──\n", sim::ms());
    return 0;
}
