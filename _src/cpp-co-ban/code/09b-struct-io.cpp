// Struct (cấu trúc dữ liệu) và Input/Output cơ bản: cin, cout, định dạng
// Dữ liệu nhập được đưa vào từ bàn phím (ở đây đã chuẩn bị sẵn – xem ô "Dữ liệu nhập")
#include <iomanip>
#include <iostream>
#include <string>

struct DiemDo {                 // gom các dữ liệu liên quan thành một kiểu mới
    std::string viTri;
    float nhietDo;
    int doAm;
};

struct KhongToiUu { char a; int b; char c; };   // trình biên dịch chèn byte đệm (padding)
struct ToiUu      { int b; char a; char c; };   // sắp trường lớn trước -> nhỏ hơn

void inDiemDo(const DiemDo& d) {
    std::cout << "  | " << std::left << std::setw(10) << d.viTri
              << " | " << std::right << std::setw(6) << std::fixed << std::setprecision(1) << d.nhietDo
              << " | " << std::setw(4) << d.doAm << " |\n";
}

int main() {
    std::cout << "== Nhập dữ liệu bằng cin ==\n";
    int soDiem;
    std::cout << "Nhập số điểm đo: ";
    std::cin >> soDiem;
    std::cout << soDiem << "\n";

    DiemDo ds[10];
    for (int i = 0; i < soDiem && i < 10; i++) {
        std::cout << "Điểm " << i + 1 << " (vị trí nhiệt-độ độ-ẩm): ";
        std::cin >> ds[i].viTri >> ds[i].nhietDo >> ds[i].doAm;
        std::cout << ds[i].viTri << " " << ds[i].nhietDo << " " << ds[i].doAm << "\n";
    }

    std::cout << "\n== In bảng có định dạng (iomanip) ==\n";
    std::cout << "  +------------+--------+------+\n";
    std::cout << "  | Vị trí     |   T°C  |  H%  |\n";
    std::cout << "  +------------+--------+------+\n";
    float tong = 0;
    for (int i = 0; i < soDiem; i++) { inDiemDo(ds[i]); tong += ds[i].nhietDo; }
    std::cout << "  +------------+--------+------+\n";
    std::cout << "  Nhiệt độ trung bình: " << tong / soDiem << "°C\n";

    std::cout << "\n== Struct lồng nhau, khởi tạo nhanh, gán cả struct ==\n";
    struct ThietBi { int id; DiemDo docGanNhat; };
    ThietBi tb = {7, {"Vuon", 30.5f, 70}};
    ThietBi banSao = tb;                      // sao chép toàn bộ các trường
    banSao.docGanNhat.nhietDo = 0;
    std::cout << "  tb.docGanNhat.nhietDo = " << tb.docGanNhat.nhietDo << " (bản sao độc lập)\n";

    std::cout << "\n== Kích thước struct và padding ==\n";
    std::cout << "  sizeof(KhongToiUu) = " << sizeof(KhongToiUu) << ", sizeof(ToiUu) = " << sizeof(ToiUu) << "\n";

    std::cout << "\n== Các cách in số ==\n";
    int v = 255;
    std::cout << "  dec " << std::dec << v << " | hex 0x" << std::hex << std::uppercase << v
              << " | oct " << std::oct << v << std::dec << "\n";
    std::cout << "  setfill: [" << std::setfill('0') << std::setw(5) << 42 << "]" << std::setfill(' ') << "\n";
    std::cerr << "(cerr: luồng báo lỗi riêng, không bị đệm)\n";
}
