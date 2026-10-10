#include "Arduino.h"
void sim_kich_ban() {
  sim_ten_chan(4, "đèn ĐỎ");
  sim_ten_chan(5, "đèn VÀNG");
  sim_ten_chan(6, "đèn XANH");
  sim_ket_thuc_sau(7500);
}
