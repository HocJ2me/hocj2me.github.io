#include "Arduino.h"
void sim_kich_ban() {
  // Bánh xe tăng tốc: chu kỳ xung giảm dần từ 20 ms xuống 5 ms (xung vuông)
  sim_digital(27, [](uint32_t t) {
    uint32_t chuKy = t < 2000 ? 20 - t / 133 : 5;
    return (int)((t % chuKy) < chuKy / 2 ? HIGH : LOW);
  });
  sim_ket_thuc_sau(2600);
}
