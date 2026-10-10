#include "Arduino.h"
#include "thiet_bi.h"
extern WebServer server;
void sim_kich_ban() {
  sim_ten_chan(2, "đèn");
  sim_analog(34, [](uint32_t) { return 2350; });
  server.sim_yeu_cau(2200, "/");
  server.sim_yeu_cau(2600, "/den?bat=1");
  server.sim_yeu_cau(3000, "/nhiet-do");
  server.sim_yeu_cau(3400, "/den?bat=0");
  server.sim_yeu_cau(3800, "/abc");
  sim_ket_thuc_sau(4000);
}
