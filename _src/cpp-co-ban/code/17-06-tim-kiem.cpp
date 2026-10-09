// Bài 6: Tìm kiếm tuần tự và tìm kiếm nhị phân (mảng đã sắp xếp)
#include <iostream>

int timTuanTu(const int a[], int n, int x, int& buoc) {
    for (int i = 0; i < n; i++) { buoc++; if (a[i] == x) return i; }
    return -1;
}

int timNhiPhan(const int a[], int n, int x, int& buoc) {
    int trai = 0, phai = n - 1;
    while (trai <= phai) {
        buoc++;
        int giua = trai + (phai - trai) / 2;    // tránh tràn số so với (trai + phai) / 2
        if (a[giua] == x) return giua;
        if (a[giua] < x) trai = giua + 1;
        else phai = giua - 1;
    }
    return -1;
}

int main() {
    const int N = 1000;
    static int a[N];
    for (int i = 0; i < N; i++) a[i] = i * 3;   // 0, 3, 6, ... 2997
    for (int x : {2991, 1500, 1501}) {
        int b1 = 0, b2 = 0;
        int i1 = timTuanTu(a, N, x, b1);
        int i2 = timNhiPhan(a, N, x, b2);
        std::cout << "Tìm " << x << ": vị trí " << i1 << "/" << i2
                  << " | tuần tự " << b1 << " bước, nhị phân " << b2 << " bước\n";
    }
}
