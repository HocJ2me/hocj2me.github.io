// Thư viện STL: container (vector, map, set, queue, stack), iterator, thuật toán, lambda
#include <algorithm>
#include <iostream>
#include <map>
#include <numeric>
#include <queue>
#include <set>
#include <stack>
#include <string>
#include <unordered_map>
#include <vector>

int main() {
    std::cout << "== vector: mảng động ==\n";
    std::vector<int> mau = {512, 498, 530, 1023, 505, 487};
    mau.push_back(520);
    std::cout << "  size = " << mau.size() << ", phần tử cuối = " << mau.back() << "\n";
    mau.erase(std::remove(mau.begin(), mau.end(), 1023), mau.end());     // xoá giá trị nhiễu
    std::cout << "  sau khi bỏ 1023: ";
    for (int v : mau) std::cout << v << " ";
    std::cout << "\n";

    std::cout << "\n== <algorithm> & <numeric> ==\n";
    std::vector<int> sapXep = mau;
    std::sort(sapXep.begin(), sapXep.end());
    std::cout << "  sort: ";
    for (int v : sapXep) std::cout << v << " ";
    std::cout << "\n  min = " << *std::min_element(mau.begin(), mau.end())
              << ", max = " << *std::max_element(mau.begin(), mau.end())
              << ", tổng = " << std::accumulate(mau.begin(), mau.end(), 0)
              << ", trung vị = " << sapXep[sapXep.size() / 2] << "\n";
    int tren500 = std::count_if(mau.begin(), mau.end(), [](int v) { return v > 500; });
    std::cout << "  số mẫu > 500: " << tren500 << "\n";
    auto it = std::find(mau.begin(), mau.end(), 530);
    std::cout << "  tìm 530 ở vị trí " << (it - mau.begin()) << "\n";
    std::sort(sapXep.begin(), sapXep.end(), [](int a, int b) { return a > b; });
    std::cout << "  sắp giảm dần bằng lambda: " << sapXep.front() << " ... " << sapXep.back() << "\n";

    std::cout << "\n== map: từ điển có thứ tự (khoá -> giá trị) ==\n";
    std::map<std::string, int> chanThietBi = {{"led", 2}, {"coi", 4}, {"servo", 18}};
    chanThietBi["quat"] = 23;
    for (const auto& [ten, chan] : chanThietBi) std::cout << "  " << ten << " -> chân " << chan << "\n";
    std::cout << "  có 'relay'? " << std::boolalpha << (chanThietBi.count("relay") > 0) << "\n";

    std::cout << "\n== unordered_map: đếm tần suất lệnh ==\n";
    std::unordered_map<char, int> dem;
    for (char c : std::string("FFLFRBFFS")) dem[c]++;
    std::cout << "  lệnh 'F' xuất hiện " << dem['F'] << " lần\n";

    std::cout << "\n== set: tập hợp không trùng, tự sắp xếp ==\n";
    std::set<int> diaChiI2C = {0x76, 0x3C, 0x68, 0x3C};
    std::cout << "  thiết bị I2C:";
    for (int a : diaChiI2C) std::cout << " 0x" << std::hex << a << std::dec;
    std::cout << " (" << diaChiI2C.size() << " thiết bị)\n";

    std::cout << "\n== queue (FIFO) và stack (LIFO) ==\n";
    std::queue<std::string> lenh;
    lenh.push("tiến"); lenh.push("rẽ trái"); lenh.push("dừng");
    std::cout << "  queue lấy ra: ";
    while (!lenh.empty()) { std::cout << lenh.front() << " | "; lenh.pop(); }
    std::stack<std::string> lichSu;
    lichSu.push("mở menu"); lichSu.push("chọn WiFi"); lichSu.push("nhập mật khẩu");
    std::cout << "\n  stack (nút Back): ";
    while (!lichSu.empty()) { std::cout << lichSu.top() << " | "; lichSu.pop(); }
    std::cout << "\n";

    std::cout << "\n== priority_queue: lấy việc ưu tiên cao nhất trước ==\n";
    std::priority_queue<std::pair<int, std::string>> viec;
    viec.push({1, "cập nhật màn hình"});
    viec.push({9, "CẢNH BÁO CHÁY"});
    viec.push({5, "gửi dữ liệu MQTT"});
    while (!viec.empty()) { std::cout << "  [" << viec.top().first << "] " << viec.top().second << "\n"; viec.pop(); }
}
