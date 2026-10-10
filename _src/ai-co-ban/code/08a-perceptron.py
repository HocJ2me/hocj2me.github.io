"""Bài 8 – Nơ-ron nhân tạo (perceptron): học hàm AND, OR – và thất bại với XOR."""
import numpy as np

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
BANG = {"AND": [0, 0, 0, 1], "OR": [0, 1, 1, 1], "XOR": [0, 1, 1, 0]}


def huan_luyen(y, so_vong=20, toc_do=0.2):
    w = np.zeros(2)
    b = 0.0
    for _ in range(so_vong):
        for xi, yi in zip(X, y):
            ra = 1 if xi @ w + b > 0 else 0       # nơ-ron: tổng có trọng số -> hàm bước
            loi = yi - ra
            w += toc_do * loi * xi                 # luật học perceptron: chỉnh trọng số theo lỗi
            b += toc_do * loi
    return w, b


for ten, y in BANG.items():
    w, b = huan_luyen(np.array(y))
    ra = [1 if xi @ w + b > 0 else 0 for xi in X]
    dung = sum(r == t for r, t in zip(ra, y))
    print(f"{ten:<4}: w = {w.round(2)}, b = {b:.2f} -> đầu ra {ra} (mong muốn {y}) – đúng {dung}/4"
          + ("" if dung == 4 else "  ✗ một nơ-ron KHÔNG làm được"))
print("\nXOR không chia được bằng MỘT đường thẳng -> cần nhiều nơ-ron xếp thành nhiều lớp (bài tiếp theo).")
