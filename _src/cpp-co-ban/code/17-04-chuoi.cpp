// Bài 4: Đảo ngược chuỗi, kiểm tra chuỗi đối xứng (palindrome), đếm nguyên âm – dùng chuỗi kiểu C
#include <cctype>
#include <cstring>
#include <iostream>

void daoChuoi(char* s) {
    int i = 0, j = std::strlen(s) - 1;
    while (i < j) {
        char t = s[i]; s[i] = s[j]; s[j] = t;    // hoán đổi hai đầu, tiến vào giữa
        i++; j--;
    }
}

bool doiXung(const char* s) {
    int i = 0, j = std::strlen(s) - 1;
    while (i < j) {
        while (i < j && !std::isalnum((unsigned char)s[i])) i++;   // bỏ qua dấu cách, dấu câu
        while (i < j && !std::isalnum((unsigned char)s[j])) j--;
        if (std::tolower((unsigned char)s[i]) != std::tolower((unsigned char)s[j])) return false;
        i++; j--;
    }
    return true;
}

int demNguyenAm(const char* s) {
    int dem = 0;
    for (; *s; s++) if (std::strchr("aeiouAEIOU", *s)) dem++;
    return dem;
}

int main() {
    char s[] = "Arduino";
    daoChuoi(s);
    std::cout << "Đảo \"Arduino\" -> \"" << s << "\"\n";
    for (const char* t : {"radar", "Never odd or even", "ESP32"})
        std::cout << "\"" << t << "\" đối xứng? " << (doiXung(t) ? "có" : "không") << "\n";
    std::cout << "Số nguyên âm trong \"Embedded Programming\": " << demNguyenAm("Embedded Programming") << "\n";
}
