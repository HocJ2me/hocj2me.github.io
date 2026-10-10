#include "Arduino.h"
void sim_kich_ban() {
  sim_ten_chan(13, "LED");
  // Người dùng nhấn 3 lần; mỗi lần nhấn tiếp điểm nảy loạn xạ trong 8 ms đầu
  sim_digital(2, sim_nut_nhan({{300, 200}, {900, 150}, {1600, 400}}, 8));
  sim_ket_thuc_sau(2300);
}
