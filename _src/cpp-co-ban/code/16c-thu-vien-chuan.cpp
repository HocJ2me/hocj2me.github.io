// Một vòng thư viện chuẩn C++ hay dùng: <optional>, <variant>, <tuple>, <string_view>, <bitset>,
// <array>, <functional>, <cstring>/<cstdlib> (thư viện C) – và ghép lại thành bộ phân tích gói tin
#include <array>
#include <bitset>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <optional>
#include <string>
#include <string_view>
#include <tuple>
#include <variant>

// string_view: "nhìn" vào chuỗi có sẵn, không sao chép – tiết kiệm RAM
std::string_view layTen(std::string_view lenh) { return lenh.substr(0, lenh.find(':')); }

// tuple / structured binding: trả về nhiều giá trị
std::tuple<float, float, bool> docDht() { return {28.6f, 64.0f, true}; }

// variant: một biến chứa MỘT trong nhiều kiểu (an toàn hơn union)
using GiaTri = std::variant<int, float, std::string>;
void inGiaTri(const GiaTri& g) {
    if (auto p = std::get_if<int>(&g))              std::cout << "  int: " << *p << "\n";
    else if (auto p = std::get_if<float>(&g))       std::cout << "  float: " << *p << "\n";
    else                                            std::cout << "  string: " << std::get<std::string>(g) << "\n";
}

// optional: có thể "không có giá trị"
std::optional<int> timChan(std::string_view ten) {
    if (ten == "led") return 2;
    if (ten == "coi") return 4;
    return std::nullopt;
}

int main() {
    std::cout << "== string_view ==\n";
    std::cout << "  layTen(\"SERVO:90\") = " << layTen("SERVO:90") << "\n";

    std::cout << "\n== tuple + structured binding ==\n";
    auto [t, h, ok] = docDht();
    std::cout << "  T = " << t << ", H = " << h << ", hợp lệ = " << std::boolalpha << ok << "\n";

    std::cout << "\n== variant ==\n";
    for (GiaTri g : {GiaTri{42}, GiaTri{3.5f}, GiaTri{std::string("OK")}}) inGiaTri(g);

    std::cout << "\n== optional ==\n";
    for (auto ten : {"led", "relay"}) {
        auto chan = timChan(ten);
        std::cout << "  " << ten << " -> " << (chan ? "chân " + std::to_string(*chan) : "không có") << "\n";
    }
    std::cout << "  value_or: " << timChan("relay").value_or(-1) << "\n";

    std::cout << "\n== bitset: thao tác cờ trạng thái ==\n";
    std::bitset<8> co;                       // 8 cờ: bit0 WiFi, bit1 MQTT, bit2 SD...
    co.set(0); co.set(2);
    std::cout << "  co = " << co << ", số cờ bật = " << co.count() << ", MQTT? " << co.test(1) << "\n";

    std::cout << "\n== Thư viện C trong C++: <cstring>, <cstdlib> ==\n";
    char goi[] = "T=28;H=64;P=1012";
    for (char* tok = std::strtok(goi, ";"); tok; tok = std::strtok(nullptr, ";")) {
        std::cout << "  " << tok[0] << " = " << std::atoi(tok + 2) << "\n";
    }
    std::array<uint8_t, 4> a{}, b{};
    a = {1, 2, 3, 4};
    std::memcpy(b.data(), a.data(), a.size());
    std::cout << "  memcpy xong, memcmp = " << std::memcmp(a.data(), b.data(), 4) << " (0 = giống nhau)\n";
}
