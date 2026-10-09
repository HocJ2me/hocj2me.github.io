// Đa luồng (multithread): std::thread, data race, mutex, atomic, producer–consumer với condition_variable
// Cùng các khái niệm này sẽ gặp lại trong khóa FreeRTOS (task, mutex, queue).
#include <atomic>
#include <condition_variable>
#include <iostream>
#include <mutex>
#include <queue>
#include <thread>
#include <vector>

int demKhongAnToan = 0;
int demCoMutex = 0;
std::atomic<int> demAtomic{0};
std::mutex khoa;

void tangKhongAnToan() { for (int i = 0; i < 100000; i++) demKhongAnToan++; }   // data race!
void tangCoMutex()     { for (int i = 0; i < 100000; i++) { std::lock_guard<std::mutex> lk(khoa); demCoMutex++; } }
void tangAtomic()      { for (int i = 0; i < 100000; i++) demAtomic++; }

int main() {
    std::cout << "== Tạo và join luồng ==\n";
    std::thread t([] { std::cout << "  xin chào từ luồng phụ\n"; });
    t.join();                                       // chờ luồng phụ kết thúc
    std::cout << "  luồng chính tiếp tục\n";

    std::cout << "\n== 4 luồng cùng tăng một biến 100 000 lần (kỳ vọng 400 000) ==\n";
    auto chay4 = [](void (*f)()) {
        std::vector<std::thread> ds;
        for (int i = 0; i < 4; i++) ds.emplace_back(f);
        for (auto& th : ds) th.join();
    };
    chay4(tangKhongAnToan);
    chay4(tangCoMutex);
    chay4(tangAtomic);
    std::cout << "  không bảo vệ : " << (demKhongAnToan == 400000 ? "400000 (may mắn)" : "SAI – bị mất lượt cộng") << "\n";
    std::cout << "  có mutex     : " << demCoMutex << "\n";
    std::cout << "  std::atomic  : " << demAtomic << "\n";

    std::cout << "\n== Producer–consumer: luồng đọc cảm biến -> hàng đợi -> luồng xử lý ==\n";
    std::queue<int> hangDoi;
    std::mutex m;
    std::condition_variable cv;
    bool xong = false;

    std::thread sanXuat([&] {
        for (int i = 1; i <= 5; i++) {
            {
                std::lock_guard<std::mutex> lk(m);
                hangDoi.push(500 + i * 10);
            }
            cv.notify_one();                         // đánh thức consumer
        }
        { std::lock_guard<std::mutex> lk(m); xong = true; }
        cv.notify_one();
    });
    std::thread tieuThu([&] {
        while (true) {
            std::unique_lock<std::mutex> lk(m);
            cv.wait(lk, [&] { return !hangDoi.empty() || xong; });   // ngủ tới khi có dữ liệu
            while (!hangDoi.empty()) {
                std::cout << "  xử lý mẫu " << hangDoi.front() << "\n";
                hangDoi.pop();
            }
            if (xong) break;
        }
    });
    sanXuat.join();
    tieuThu.join();
    std::cout << "  Phần cứng có " << std::thread::hardware_concurrency() << " luồng; ESP32 có 2 nhân\n";
}
