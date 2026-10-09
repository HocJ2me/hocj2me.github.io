// Con trỏ với địa chỉ – địa chỉ với con trỏ – con trỏ tới con trỏ
// (Địa chỉ thật thay đổi mỗi lần chạy nên ví dụ chỉ in KHOẢNG CÁCH và kết quả so sánh)
#include <cstdint>
#include <iostream>

void hoanDoi(int* a, int* b) {     // đổi chỗ hai biến qua con trỏ
    int tam = *a;
    *a = *b;
    *b = tam;
}

void capPhatLai(int** pp, int* moi) {   // con trỏ tới con trỏ: hàm SỬA ĐƯỢC chính con trỏ của bên gọi
    *pp = moi;
}

int main() {
    std::cout << std::boolalpha;
    std::cout << "== & lấy địa chỉ, * truy cập giá trị tại địa chỉ ==\n";
    int nhietDo = 28;
    int* p = &nhietDo;                   // p chứa ĐỊA CHỈ của nhietDo
    std::cout << "  *p = " << *p << "\n";
    *p = 35;                             // ghi qua con trỏ = ghi vào nhietDo
    std::cout << "  sau *p = 35: nhietDo = " << nhietDo << "\n";
    std::cout << "  p == &nhietDo ? " << (p == &nhietDo) << "\n";
    std::cout << "  sizeof(p) = " << sizeof(p) << " byte (máy 64 bit; ESP32/STM32 là 4 byte)\n";

    std::cout << "\n== nullptr: con trỏ không trỏ vào đâu ==\n";
    int* q = nullptr;
    if (q == nullptr) std::cout << "  q rỗng – luôn kiểm tra trước khi dùng *q\n";

    std::cout << "\n== Con trỏ và mảng: tên mảng là địa chỉ phần tử đầu ==\n";
    int adc[5] = {100, 200, 300, 400, 500};
    int* pa = adc;                       // tương đương &adc[0]
    std::cout << "  *pa = " << *pa << ", *(pa + 2) = " << *(pa + 2) << ", pa[3] = " << pa[3] << "\n";
    std::cout << "  (pa + 1) cách pa bao nhiêu byte? "
              << (reinterpret_cast<uintptr_t>(pa + 1) - reinterpret_cast<uintptr_t>(pa))
              << " = sizeof(int)\n";
    std::cout << "  Duyệt bằng con trỏ: ";
    for (int* it = adc; it != adc + 5; ++it) std::cout << *it << " ";
    std::cout << "\n  Số phần tử giữa hai con trỏ: " << (&adc[4] - &adc[0]) << "\n";

    std::cout << "\n== Truyền con trỏ vào hàm ==\n";
    int a = 1, b = 2;
    hoanDoi(&a, &b);
    std::cout << "  sau hoanDoi: a = " << a << ", b = " << b << "\n";

    std::cout << "\n== Con trỏ tới con trỏ (int**) ==\n";
    int x = 10, y = 20;
    int* px = &x;
    int** ppx = &px;                     // ppx trỏ tới biến con trỏ px
    std::cout << "  **ppx = " << **ppx << "\n";
    capPhatLai(&px, &y);                 // hàm đổi px sang trỏ y
    std::cout << "  sau capPhatLai: *px = " << *px << ", px == &y ? " << (px == &y) << "\n";

    std::cout << "\n== Mảng con trỏ: bảng tên chế độ ==\n";
    const char* cheDo[] = {"TẮT", "TỰ ĐỘNG", "THỦ CÔNG"};
    for (int i = 0; i < 3; i++) std::cout << "  cheDo[" << i << "] = " << cheDo[i] << "\n";

    std::cout << "\n== const với con trỏ ==\n";
    const int* chiDoc = &x;   // không sửa được GIÁ TRỊ qua con trỏ:  *chiDoc = 5 -> lỗi
    int* const coDinh = &x;   // không đổi được ĐỊA CHỈ:               coDinh = &y -> lỗi
    *coDinh = 11;
    std::cout << "  *chiDoc = " << *chiDoc << "\n";
}
