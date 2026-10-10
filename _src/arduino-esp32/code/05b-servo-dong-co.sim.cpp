#include "Arduino.h"
void sim_kich_ban() {
  sim_ten_chan(25, "động cơ");
  sim_ten_chan(18, "servo");
  // Người dùng vặn biến trở từ 0 lên hết rồi về giữa
  sim_analog(34, [](uint32_t t) { return t < 1600 ? (int)(t * 2.55) : 2048; });
  sim_ket_thuc_sau(2100);
}
