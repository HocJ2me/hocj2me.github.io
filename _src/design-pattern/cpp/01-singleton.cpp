// Singleton – C++17. Biên dịch: g++ -std=c++17 01-singleton.cpp
// Trên Arduino/ESP32: thay std::cout bằng Serial.println.
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <thread>
#include <mutex>
#include <vector>

// Cách 1 – "Meyers Singleton": biến static cục bộ trong hàm.
// Từ C++11, chuẩn đảm bảo việc khởi tạo biến static cục bộ là thread-safe
// và chỉ diễn ra MỘT lần, ở lần gọi đầu tiên (lazy).
class AppConfig {
public:
    static AppConfig& getInstance() {
        static AppConfig instance;          // nằm ở vùng nhớ tĩnh, không dùng heap
        return instance;
    }
    // Cấm sao chép và gán -> không thể tạo bản thứ hai
    AppConfig(const AppConfig&) = delete;
    AppConfig& operator=(const AppConfig&) = delete;

    void set(const std::string& k, const std::string& v) { props_[k] = v; }
    std::string get(const std::string& k) const { return props_.at(k); }

private:
    AppConfig() { std::cout << ">> AppConfig được khởi tạo (chỉ 1 lần)\n"; }
    std::map<std::string, std::string> props_;
};

// Cách 2 – Singleton quản lý một ngoại vi phần cứng (UART giả lập).
// Trên vi điều khiển chỉ có MỘT bộ UART0 thật, nên đối tượng điều khiển nó
// cũng chỉ nên có một. std::call_once đảm bảo init phần cứng chạy đúng 1 lần.
class Uart0 {
public:
    static Uart0& getInstance() {
        static Uart0 instance;
        std::call_once(initFlag_, [] { instance.initHardware(115200); });
        return instance;
    }
    Uart0(const Uart0&) = delete;
    Uart0& operator=(const Uart0&) = delete;

    static inline int initCount = 0;
private:
    Uart0() = default;
    void initHardware(int baud) { ++initCount; baud_ = baud; /* cấu hình thanh ghi... */ }
    int baud_ = 0;
    static inline std::once_flag initFlag_;
};

int main() {
    AppConfig& c1 = AppConfig::getInstance();
    AppConfig& c2 = AppConfig::getInstance();
    c1.set("wifi.ssid", "BKSTAR-Lab");
    std::cout << "&c1 == &c2 ? " << std::boolalpha << (&c1 == &c2) << "\n";
    std::cout << "Đọc qua c2: wifi.ssid = " << c2.get("wifi.ssid") << "\n";

    // 50 luồng cùng gọi getInstance()
    std::set<const void*> addrs;
    std::mutex m;
    std::vector<std::thread> threads;
    for (int i = 0; i < 50; ++i)
        threads.emplace_back([&] {
            const void* p = &Uart0::getInstance();
            std::lock_guard<std::mutex> lock(m);
            addrs.insert(p);
        });
    for (auto& t : threads) t.join();
    std::cout << "Số địa chỉ Uart0 khác nhau từ 50 luồng: " << addrs.size() << "\n";
    std::cout << "Số lần initHardware() chạy: " << Uart0::initCount << "\n";

    // AppConfig x;                 // LỖI biên dịch: constructor là private
    // AppConfig y = c1;            // LỖI biên dịch: copy constructor đã bị delete
}
