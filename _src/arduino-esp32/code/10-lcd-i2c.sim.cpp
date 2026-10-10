#include "Arduino.h"
#include "thiet_bi.h"
void sim_kich_ban() {
  sim_dht_nhiet = [](uint32_t t) { return 28.3f + t / 4000.0f; };
  sim_dht_am = [](uint32_t t) { return 64.0f - t / 1000.0f; };
  sim_ket_thuc_sau(5600);
}
