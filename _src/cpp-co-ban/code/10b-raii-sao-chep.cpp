// RAII (Resource Acquisition Is Initialization) và quy tắc sao chép (copy constructor, operator=)
#include <cstring>
#include <iostream>

// Ví dụ RAII: "khoá bus I2C" – lấy khi tạo, TỰ trả khi huỷ, kể cả khi return sớm
class I2CLock {
public:
    I2CLock()  { std::cout << "    [lock]   chiếm bus I2C\n"; }
    ~I2CLock() { std::cout << "    [unlock] trả bus I2C\n"; }
};

bool docCamBien(int diaChi) {
    I2CLock khoa;                          // chiếm bus
    std::cout << "    đọc thiết bị 0x" << std::hex << diaChi << std::dec << "\n";
    if (diaChi == 0x77) {
        std::cout << "    thiết bị không phản hồi -> return sớm\n";
        return false;                      // bus VẪN được trả nhờ destructor
    }
    return true;
}

// Lớp tự quản lý bộ nhớ -> cần viết copy constructor & operator= (quy tắc 3)
class BoDem {
public:
    explicit BoDem(size_t n) : n_(n), data_(new int[n]{}) {}
    ~BoDem() { delete[] data_; }

    BoDem(const BoDem& khac) : n_(khac.n_), data_(new int[khac.n_]) {      // sao chép SÂU
        std::memcpy(data_, khac.data_, n_ * sizeof(int));
        std::cout << "  [copy constructor]\n";
    }
    BoDem& operator=(const BoDem& khac) {
        if (this != &khac) {                                                // tự gán cho chính mình
            int* moi = new int[khac.n_];
            std::memcpy(moi, khac.data_, khac.n_ * sizeof(int));
            delete[] data_;
            data_ = moi;
            n_ = khac.n_;
        }
        std::cout << "  [operator=]\n";
        return *this;
    }

    int& operator[](size_t i) { return data_[i]; }
private:
    size_t n_;
    int* data_;
};

// Lớp quản lý phần cứng duy nhất thì nên CẤM sao chép
class UartPort {
public:
    UartPort() = default;
    UartPort(const UartPort&) = delete;
    UartPort& operator=(const UartPort&) = delete;
};

int main() {
    std::cout << "== RAII ==\n";
    bool kq1 = docCamBien(0x76);
    std::cout << "  -> kết quả " << std::boolalpha << kq1 << "\n";
    bool kq2 = docCamBien(0x77);
    std::cout << "  -> kết quả " << kq2 << "\n";

    std::cout << "\n== Sao chép sâu ==\n";
    BoDem a(3);
    a[0] = 10;
    BoDem b = a;            // copy constructor
    b[0] = 99;
    std::cout << "  a[0] = " << a[0] << ", b[0] = " << b[0] << " -> hai bộ đệm độc lập\n";
    BoDem c(1);
    c = a;                  // operator=
    std::cout << "  c[0] = " << c[0] << "\n";

    std::cout << "\n== Cấm sao chép ==\n";
    [[maybe_unused]] UartPort uart0;
    // UartPort uart1 = uart0;   // LỖI biên dịch: copy constructor đã bị delete
    std::cout << "  UartPort không thể sao chép -> tránh 2 đối tượng cùng điều khiển một cổng\n";
}
