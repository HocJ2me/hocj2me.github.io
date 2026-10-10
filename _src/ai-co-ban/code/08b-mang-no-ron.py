"""Bài 8 – Mạng nơ-ron 2 lớp tự viết bằng numpy, huấn luyện bằng LAN TRUYỀN NGƯỢC (backpropagation) để học XOR."""
import numpy as np

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
y = np.array([[0], [1], [1], [0]], dtype=float)


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


rng = np.random.default_rng(1)
W1 = rng.normal(0, 1, (2, 4))        # lớp ẩn: 2 đầu vào -> 4 nơ-ron
b1 = np.zeros(4)
W2 = rng.normal(0, 1, (4, 1))        # lớp ra: 4 -> 1
b2 = np.zeros(1)
toc_do = 1.0

for vong in range(5001):
    # ----- lan truyền xuôi -----
    h = sigmoid(X @ W1 + b1)
    ra = sigmoid(h @ W2 + b2)
    mat_mat = np.mean((ra - y) ** 2)
    # ----- lan truyền ngược: đạo hàm theo quy tắc chuỗi -----
    d_ra = 2 * (ra - y) / len(X) * ra * (1 - ra)
    d_W2 = h.T @ d_ra
    d_b2 = d_ra.sum(axis=0)
    d_h = d_ra @ W2.T * h * (1 - h)
    d_W1 = X.T @ d_h
    d_b1 = d_h.sum(axis=0)
    # ----- cập nhật trọng số -----
    W2 -= toc_do * d_W2; b2 -= toc_do * d_b2
    W1 -= toc_do * d_W1; b1 -= toc_do * d_b1
    if vong in (0, 500, 1000, 2000, 5000):
        print(f"vòng {vong:>4}: mất mát = {mat_mat:.4f}")

print("\nKết quả sau huấn luyện:")
for xi, ri in zip(X, sigmoid(sigmoid(X @ W1 + b1) @ W2 + b2)):
    print(f"  {int(xi[0])} XOR {int(xi[1])} -> {ri[0]:.3f} -> {int(ri[0] > 0.5)}")
print(f"Số tham số của mạng: {W1.size + b1.size + W2.size + b2.size}")
