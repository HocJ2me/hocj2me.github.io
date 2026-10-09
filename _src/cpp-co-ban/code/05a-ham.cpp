// Hàm: khai báo, định nghĩa, truyền tham trị / tham chiếu / con trỏ, mặc định, nạp chồng, đệ quy, inline
#include <iostream>

// 1. KHAI BÁO (prototype) trước – ĐỊNH NGHĨA ở cuối file. Thường đặt khai báo trong file .h
float celsiusToF(float c);

// 2. Truyền THAM TRỊ: hàm nhận BẢN SAO, sửa không ảnh hưởng biến gốc
void tangThamTri(int x) { x++; }

// 3. Truyền THAM CHIẾU: hàm làm việc trên CHÍNH biến gốc
void tangThamChieu(int& x) { x++; }

// 4. Truyền CON TRỎ: giống tham chiếu nhưng phải dùng * và có thể là nullptr
void tangConTro(int* x) { if (x) (*x)++; }

// 5. "Trả về nhiều giá trị" bằng tham chiếu đầu ra
void minMax(const int a[], int n, int& mn, int& mx) {
    mn = mx = a[0];
    for (int i = 1; i < n; i++) {
        if (a[i] < mn) mn = a[i];
        if (a[i] > mx) mx = a[i];
    }
}

// 6. Tham số MẶC ĐỊNH (phải nằm ở cuối danh sách)
void nhayLed(int pin, int soLan = 3, int msMoiLan = 200) {
    std::cout << "  Nháy LED chân " << pin << " x" << soLan << " lần, mỗi lần " << msMoiLan << "ms\n";
}

// 7. NẠP CHỒNG hàm: cùng tên, khác kiểu/số tham số
int binhPhuong(int x)       { return x * x; }
double binhPhuong(double x) { return x * x; }

// 8. ĐỆ QUY: hàm tự gọi chính nó – phải có điều kiện dừng
unsigned long giaiThua(unsigned n) { return n <= 1 ? 1 : n * giaiThua(n - 1); }

// 9. inline / constexpr: gợi ý chèn thân hàm tại chỗ gọi, tránh chi phí gọi hàm
constexpr int adcToMilliVolt(int adc) { return adc * 3300 / 4095; }

int main() {
    std::cout << "== Gọi hàm đã khai báo trước ==\n";
    std::cout << "  30°C = " << celsiusToF(30) << "°F\n";

    std::cout << "\n== Tham trị / tham chiếu / con trỏ ==\n";
    int a = 10;
    tangThamTri(a);    std::cout << "  sau tangThamTri:  a = " << a << "\n";
    tangThamChieu(a);  std::cout << "  sau tangThamChieu: a = " << a << "\n";
    tangConTro(&a);    std::cout << "  sau tangConTro:   a = " << a << "\n";

    int mau[] = {23, 7, 91, 45, 12};
    int mn, mx;
    minMax(mau, 5, mn, mx);
    std::cout << "  min = " << mn << ", max = " << mx << "\n";

    std::cout << "\n== Tham số mặc định ==\n";
    nhayLed(13);
    nhayLed(13, 5);
    nhayLed(2, 1, 1000);

    std::cout << "\n== Nạp chồng ==\n";
    std::cout << "  binhPhuong(7) = " << binhPhuong(7) << ", binhPhuong(1.5) = " << binhPhuong(1.5) << "\n";

    std::cout << "\n== Đệ quy ==\n";
    for (unsigned n : {0u, 5u, 10u}) std::cout << "  " << n << "! = " << giaiThua(n) << "\n";

    std::cout << "\n== constexpr: tính sẵn lúc biên dịch ==\n";
    constexpr int mv = adcToMilliVolt(2048);
    std::cout << "  ADC 2048 ≈ " << mv << " mV\n";

    std::cout << "\n== Lambda: hàm không tên, viết ngay tại chỗ ==\n";
    auto loc = [](int v) { return v > 50; };
    for (int v : mau) if (loc(v)) std::cout << "  " << v << " > 50\n";
}

// ĐỊNH NGHĨA hàm đã khai báo ở đầu file
float celsiusToF(float c) {
    return c * 9 / 5 + 32;
}
