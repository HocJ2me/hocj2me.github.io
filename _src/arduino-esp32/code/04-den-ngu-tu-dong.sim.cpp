#include "Arduino.h"
void sim_kich_ban() {
  sim_ten_chan(2, "đèn ngủ");
  // Trời tối dần: ánh sáng giảm từ 3200 xuống ~600 trong 3 giây
  sim_analog(34, [](uint32_t t) { return (int)(3200 - t * 0.9); });
  sim_analog(35, [](uint32_t) { return 1500; });       // biến trở để ở 1500
  sim_ket_thuc_sau(3100);
}
