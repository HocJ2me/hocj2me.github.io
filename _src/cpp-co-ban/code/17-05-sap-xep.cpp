// Bài 5: Sắp xếp mảng – nổi bọt (bubble sort) và chèn (insertion sort), đếm số phép so sánh
#include <iostream>

int bubbleSort(int a[], int n) {
    int soSanh = 0;
    for (int i = 0; i < n - 1; i++) {
        bool coDoi = false;
        for (int j = 0; j < n - 1 - i; j++) {
            soSanh++;
            if (a[j] > a[j + 1]) { int t = a[j]; a[j] = a[j + 1]; a[j + 1] = t; coDoi = true; }
        }
        if (!coDoi) break;                 // đã có thứ tự -> dừng sớm
    }
    return soSanh;
}

int insertionSort(int a[], int n) {
    int soSanh = 0;
    for (int i = 1; i < n; i++) {
        int x = a[i], j = i - 1;
        while (j >= 0 && (++soSanh, a[j] > x)) { a[j + 1] = a[j]; j--; }
        a[j + 1] = x;
    }
    return soSanh;
}

void in(const char* ten, const int a[], int n) {
    std::cout << ten;
    for (int i = 0; i < n; i++) std::cout << a[i] << " ";
    std::cout << "\n";
}

int main() {
    int a[] = {64, 25, 12, 22, 11, 90, 3};
    int b[] = {64, 25, 12, 22, 11, 90, 3};
    in("Ban đầu      : ", a, 7);
    int s1 = bubbleSort(a, 7);
    int s2 = insertionSort(b, 7);
    in("Bubble sort  : ", a, 7);
    in("Insertion    : ", b, 7);
    std::cout << "Số phép so sánh: bubble = " << s1 << ", insertion = " << s2 << "\n";
}
