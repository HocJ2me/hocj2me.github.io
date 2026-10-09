// Bài 10: Ma trận – cộng, nhân, chuyển vị (ứng dụng: xoay toạ độ, xử lý ảnh nhỏ)
#include <iomanip>
#include <iostream>

const int N = 3;

void in(const char* ten, const int m[N][N]) {
    std::cout << ten << ":\n";
    for (int i = 0; i < N; i++) {
        std::cout << "  ";
        for (int j = 0; j < N; j++) std::cout << std::setw(5) << m[i][j];
        std::cout << "\n";
    }
}

void nhan(const int a[N][N], const int b[N][N], int kq[N][N]) {
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++) {
            kq[i][j] = 0;
            for (int k = 0; k < N; k++) kq[i][j] += a[i][k] * b[k][j];   // hàng i của A nhân cột j của B
        }
}

void chuyenVi(const int a[N][N], int kq[N][N]) {
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++) kq[j][i] = a[i][j];
}

int main() {
    int A[N][N] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
    int B[N][N] = {{9, 8, 7}, {6, 5, 4}, {3, 2, 1}};
    int C[N][N], T[N][N];
    nhan(A, B, C);
    chuyenVi(A, T);
    in("A", A);
    in("A x B", C);
    in("Chuyển vị của A", T);
    int vet = 0;
    for (int i = 0; i < N; i++) vet += A[i][i];
    std::cout << "Vết (tổng đường chéo) của A = " << vet << "\n";
}
