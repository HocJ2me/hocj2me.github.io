// Tham chiếu (reference): bí danh của một biến – so sánh với con trỏ
#include <iostream>
#include <string>
#include <vector>

struct CamBien { std::string ten; float giaTri; };

void hieuChinh(CamBien& cb, float lech) { cb.giaTri += lech; }     // sửa trực tiếp

// const & : đọc nhanh (không sao chép) nhưng không sửa được – cách truyền object lớn chuẩn nhất
void inCamBien(const CamBien& cb) {
    std::cout << "  " << cb.ten << " = " << cb.giaTri << "\n";
    // cb.giaTri = 0;   // LỖI: cb là const
}

// Trả về tham chiếu -> có thể gán vào kết quả của hàm
int& phanTu(std::vector<int>& v, size_t i) { return v[i]; }

int main() {
    std::cout << "== Tham chiếu là tên khác của cùng một biến ==\n";
    int tocDo = 100;
    int& rTocDo = tocDo;            // PHẢI khởi tạo ngay, và không thể đổi sang biến khác
    rTocDo = 150;
    std::cout << "  tocDo = " << tocDo << ", &rTocDo == &tocDo ? " << std::boolalpha << (&rTocDo == &tocDo) << "\n";

    std::cout << "\n== Truyền tham chiếu vào hàm ==\n";
    CamBien dht{"DHT22", 27.0f};
    hieuChinh(dht, -0.5f);
    inCamBien(dht);

    std::cout << "\n== Trả về tham chiếu ==\n";
    std::vector<int> ds = {1, 2, 3};
    phanTu(ds, 1) = 99;
    std::cout << "  ds[1] = " << ds[1] << "\n";

    std::cout << "\n== range-for: có & thì sửa được, không có & thì chỉ sửa bản sao ==\n";
    std::vector<CamBien> cacCamBien = {{"A0", 1.0f}, {"A1", 2.0f}};
    for (CamBien c : cacCamBien) c.giaTri *= 10;           // bản sao -> không đổi
    std::cout << "  không &: A0 = " << cacCamBien[0].giaTri << "\n";
    for (CamBien& c : cacCamBien) c.giaTri *= 10;          // tham chiếu -> đổi thật
    std::cout << "  có &   : A0 = " << cacCamBien[0].giaTri << "\n";
    for (const auto& c : cacCamBien) inCamBien(c);         // chỉ đọc: const auto&

    std::cout << "\n== Con trỏ vs tham chiếu ==\n";
    std::cout << "  Con trỏ: có thể nullptr, đổi được nơi trỏ tới, dùng *p / p->\n";
    std::cout << "  Tham chiếu: luôn gắn với một biến, không đổi được, dùng như biến thường\n";
}
