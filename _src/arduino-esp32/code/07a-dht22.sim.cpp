#include "Arduino.h"
#include "thiet_bi.h"
void sim_kich_ban() {
  sim_ten_chan(26, "quạt");
  sim_dht_nhiet = [](uint32_t t) { return 27.0f + t / 1000.0f * 1.1f; };   // nóng dần
  sim_dht_am = [](uint32_t t) { return 72.0f + t / 1000.0f * 2.0f; };
  sim_ket_thuc_sau(8100);
}
