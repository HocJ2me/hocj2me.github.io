// Bài 12: Chương trình quản lý danh sách học sinh – tổng hợp struct, mảng, hàm, sắp xếp, tìm kiếm, thống kê
#include <algorithm>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

struct HocSinh {
    std::string ten;
    std::string lop;
    float diem;
};

std::string xepLoai(float d) {
    if (d >= 8) return "Giỏi";
    if (d >= 6.5) return "Khá";
    if (d >= 5) return "Trung bình";
    return "Yếu";
}

void inDanhSach(const std::vector<HocSinh>& ds) {
    for (size_t i = 0; i < ds.size(); i++)
        std::cout << "  " << i + 1 << ". " << std::left << std::setw(10) << ds[i].ten << std::setw(6) << ds[i].lop
                  << std::right << std::fixed << std::setprecision(1) << std::setw(5) << ds[i].diem
                  << "  " << xepLoai(ds[i].diem) << "\n";
}

int main() {
    std::vector<HocSinh> ds = {
        {"An", "10A1", 8.5f}, {"Binh", "10A2", 6.0f}, {"Chi", "10A1", 9.2f},
        {"Dung", "10A2", 4.5f}, {"Giang", "10A1", 7.1f},
    };

    std::cout << "Danh sách ban đầu:\n";
    inDanhSach(ds);

    std::sort(ds.begin(), ds.end(), [](const HocSinh& a, const HocSinh& b) { return a.diem > b.diem; });
    std::cout << "\nSắp xếp theo điểm giảm dần:\n";
    inDanhSach(ds);

    float tong = 0;
    int soGioi = 0;
    for (const auto& h : ds) { tong += h.diem; if (h.diem >= 8) soGioi++; }
    std::cout << "\nĐiểm trung bình: " << tong / ds.size() << ", số học sinh giỏi: " << soGioi << "\n";

    auto it = std::find_if(ds.begin(), ds.end(), [](const HocSinh& h) { return h.ten == "Giang"; });
    if (it != ds.end()) std::cout << "Tìm thấy Giang: lớp " << it->lop << ", điểm " << it->diem << "\n";

    std::cout << "Học sinh lớp 10A1:";
    for (const auto& h : ds) if (h.lop == "10A1") std::cout << " " << h.ten;
    std::cout << "\n";
}
