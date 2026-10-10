#include "Arduino.h"
#include "thiet_bi.h"
extern PubSubClient mqtt;
void sim_kich_ban() {
  sim_ten_chan(2, "đèn hiên");
  sim_ten_chan(26, "quạt");
  sim_dht_nhiet = [](uint32_t t) { return 29.0f + t / 1000.0f; };
  sim_dht_am = [](uint32_t) { return 65.0f; };
  sim_analog(34, [](uint32_t t) { return t < 5000 ? 2500 : 900; });     // chiều tối trời tắt nắng
  mqtt.sim_tin_den(4500, "nha/dieu-khien", "che-do:thu-cong");
  mqtt.sim_tin_den(5200, "nha/dieu-khien", "den:bat");
  mqtt.sim_tin_den(7800, "nha/dieu-khien", "che-do:tu-dong");
  sim_ket_thuc_sau(9700);
}
