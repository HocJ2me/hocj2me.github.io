// Object Pool – C++17. Rất phổ biến trong firmware: KHÔNG malloc/new lúc chạy,
// mọi đối tượng nằm sẵn trong một mảng tĩnh có kích thước biết trước khi biên dịch.
#include <array>
#include <cstdio>
#include <iostream>

class DbConnection {                     // trên MCU có thể là: gói tin, buffer DMA, timer phần mềm...
public:
    static inline int created = 0;
    void open()  { id_ = ++created; std::cout << "  (khởi tạo kết nối #" << id_ << " – tốn ~200ms)\n"; }
    void query(const char* sql) { ++useCount_; std::cout << "  #" << id_ << " chạy: " << sql << "\n"; }
    void reset() { /* xoá trạng thái dở dang */ }
    void print() const { std::cout << "Conn#" << id_ << "(đã dùng " << useCount_ << " lần)"; }
private:
    int id_ = 0, useCount_ = 0;
};

template <typename T, size_t N>
class ObjectPool {
public:
    // Trả về nullptr khi pool đầy – firmware không ném exception
    T* acquire() {
        for (size_t i = 0; i < N; ++i) {
            if (!inUse_[i]) {
                if (!initialized_[i]) { items_[i].open(); initialized_[i] = true; }  // khởi tạo lười, 1 lần
                inUse_[i] = true;
                return &items_[i];
            }
        }
        return nullptr;
    }
    void release(T* obj) {
        size_t i = obj - items_.data();            // tính chỉ số từ địa chỉ
        if (i < N && inUse_[i]) { obj->reset(); inUse_[i] = false; }
    }
    void printStatus() const {
        size_t used = 0;
        for (bool b : inUse_) used += b;
        std::cout << "  [Pool] đang dùng=" << used << ", rảnh=" << N - used << ", tối đa=" << N << "\n";
    }
private:
    std::array<T, N> items_{};                     // bộ nhớ cấp phát TĨNH, biết trước lúc biên dịch
    std::array<bool, N> inUse_{};
    std::array<bool, N> initialized_{};
};

int main() {
    static ObjectPool<DbConnection, 2> pool;       // static: nằm trong .bss, không ở stack/heap

    DbConnection* a = pool.acquire();
    DbConnection* b = pool.acquire();
    a->query("SELECT * FROM students");
    b->query("SELECT * FROM courses");
    pool.printStatus();

    DbConnection* c = pool.acquire();
    std::cout << "Lấy thêm khi pool đầy -> " << (c ? "có" : "nullptr") << "\n";

    pool.release(a);
    pool.printStatus();

    DbConnection* d = pool.acquire();
    d->query("UPDATE scores SET point = 10");
    std::cout << "d có phải là a được tái sử dụng? " << std::boolalpha << (d == a) << "\n";
    pool.printStatus();
    std::cout << "Tổng số kết nối thực sự được tạo: " << DbConnection::created << "\n";
    std::cout << "Kích thước pool trong RAM: " << sizeof(pool) << " byte (cố định)\n";
}
