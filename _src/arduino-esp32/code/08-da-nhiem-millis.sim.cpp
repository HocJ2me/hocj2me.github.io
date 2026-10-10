#include "Arduino.h"
void sim_kich_ban() {
  sim_ten_chan(26, "quạt");
  sim_ten_chan(2, "LED");
  sim_analog(34, [](uint32_t t) { return t < 1500 ? 2620 : 2290; });   // ~32°C rồi ~28°C
  sim_digital(0, sim_nut_nhan({{1720, 120}, {2650, 100}}));
  sim_ket_thuc_sau(3200);
}
