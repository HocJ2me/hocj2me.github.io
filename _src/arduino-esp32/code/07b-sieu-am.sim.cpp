#include "Arduino.h"
void sim_kich_ban() {
  sim_ten_chan(19, "còi");
  // Xe lùi dần về phía tường: 80 cm -> 5 cm trong 2 giây (thời gian echo = cm * 58 µs)
  sim_pulse(18, [](uint32_t t) {
    float cm = 80 - t * 0.0375f;
    if (cm < 5) cm = 5;
    return (uint32_t)(cm * 58.3f);
  });
  sim_ket_thuc_sau(2400);
}
