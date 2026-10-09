// Mảng: một chiều, hai chiều, truyền vào hàm, std::array, bộ đệm vòng (ring buffer)
#include <array>
#include <iostream>

// Mảng truyền vào hàm sẽ "suy biến" thành con trỏ -> phải truyền kèm số phần tử
int tinhTong(const int a[], int n) {
    int s = 0;
    for (int i = 0; i < n; i++) s += a[i];
    return s;
}

// std::array giữ được kích thước, có .size(), an toàn hơn
template <size_t N>
float trungBinh(const std::array<int, N>& a) {
    long s = 0;
    for (int v : a) s += v;
    return float(s) / a.size();
}

// Bộ lọc trung bình trượt dùng bộ đệm vòng – kỹ thuật kinh điển để lọc nhiễu cảm biến
class MovingAverage {
public:
    float them(int giaTri) {
        tong_ -= buf_[viTri_];
        buf_[viTri_] = giaTri;
        tong_ += giaTri;
        viTri_ = (viTri_ + 1) % N;     // quay vòng về 0 khi tới cuối mảng
        if (dem_ < N) dem_++;
        return float(tong_) / dem_;
    }
private:
    static constexpr int N = 4;
    int buf_[N] = {0};
    int viTri_ = 0, dem_ = 0;
    long tong_ = 0;
};

int main() {
    std::cout << "== Mảng một chiều ==\n";
    int nhietDo[7] = {28, 30, 31, 29, 27, 33, 32};   // nhiệt độ 7 ngày
    int n = sizeof(nhietDo) / sizeof(nhietDo[0]);     // số phần tử = tổng byte / byte mỗi phần tử
    std::cout << "  Số phần tử: " << n << ", phần tử đầu: " << nhietDo[0] << ", cuối: " << nhietDo[n - 1] << "\n";
    std::cout << "  Tổng: " << tinhTong(nhietDo, n) << "\n";
    int chanLed[] = {2, 4, 5, 18};                    // khởi tạo không ghi kích thước
    std::cout << "  Các chân LED: ";
    for (int p : chanLed) std::cout << p << " ";
    std::cout << "\n";
    int day[5] = {1, 2};                              // phần còn lại tự = 0
    std::cout << "  day[4] = " << day[4] << "\n";
    // nhietDo[7] = 0;  // LỖI NGUY HIỂM: truy cập ngoài mảng -> ghi đè bộ nhớ khác, không báo lỗi!

    std::cout << "\n== Mảng hai chiều: bản đồ 4x6 cho robot ==\n";
    const int H = 4, W = 6;
    char banDo[H][W] = {
        {'.', '.', '#', '.', '.', '.'},
        {'.', '#', '#', '.', '#', '.'},
        {'.', '.', '.', '.', '#', '.'},
        {'#', '#', '.', '.', '.', 'G'},
    };
    int soVatCan = 0;
    for (int r = 0; r < H; r++) {
        std::cout << "  ";
        for (int c = 0; c < W; c++) {
            std::cout << banDo[r][c] << ' ';
            if (banDo[r][c] == '#') soVatCan++;
        }
        std::cout << "\n";
    }
    std::cout << "  Số ô vật cản: " << soVatCan << "\n";

    std::cout << "\n== std::array ==\n";
    std::array<int, 5> adc = {510, 520, 505, 515, 500};
    std::cout << "  size = " << adc.size() << ", trung bình = " << trungBinh(adc) << "\n";
    std::cout << "  adc.at(2) = " << adc.at(2) << " (at() kiểm tra chỉ số, an toàn hơn [])\n";

    std::cout << "\n== Lọc nhiễu bằng trung bình trượt (ring buffer) ==\n";
    MovingAverage loc;
    for (int v : {500, 502, 498, 900, 501, 499, 503}) {   // 900 là nhiễu
        std::cout << "  đọc " << v << " -> sau lọc " << loc.them(v) << "\n";
    }
}
