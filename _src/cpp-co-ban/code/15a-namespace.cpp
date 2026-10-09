// Namespace: tránh trùng tên khi ghép nhiều thư viện
#include <iostream>

namespace dht {
    float doc() { return 28.4f; }
    const char* ten = "DHT22";
}

namespace bmp {
    float doc() { return 1012.7f; }          // cùng tên doc() nhưng không xung đột
    const char* ten = "BMP280";
    namespace hieuChinh {                     // namespace lồng nhau
        float heSo = 1.002f;
    }
}

namespace robot::dongCo {                     // cú pháp lồng gọn (C++17)
    void chay() { std::cout << "  robot::dongCo::chay()\n"; }
}

namespace {                                   // namespace ẩn danh: chỉ thấy trong file này (như static)
    int biMat = 42;
}

namespace dongCoRatDaiTen { void dung() { std::cout << "  dừng động cơ\n"; } }

int main() {
    std::cout << "== Gọi bằng tên đầy đủ ==\n";
    std::cout << "  " << dht::ten << ": " << dht::doc() << "\n";
    std::cout << "  " << bmp::ten << ": " << bmp::doc() * bmp::hieuChinh::heSo << "\n";
    robot::dongCo::chay();

    std::cout << "\n== using: đưa MỘT tên vào phạm vi hiện tại ==\n";
    using std::cout;
    cout << "  dùng cout không cần std::\n";

    std::cout << "\n== Bí danh namespace ==\n";
    namespace dc = dongCoRatDaiTen;
    dc::dung();

    std::cout << "\n== Namespace ẩn danh ==\n";
    std::cout << "  biMat = " << biMat << "\n";

    std::cout << "\n  Lưu ý: tránh viết 'using namespace std;' trong file .h – dễ gây trùng tên ở nơi include.\n";
}
