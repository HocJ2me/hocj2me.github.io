"""Bài 3 – Hồi quy tuyến tính: dự đoán giá nhà theo diện tích.
Tự cài GRADIENT DESCENT bằng numpy, rồi so sánh với scikit-learn."""
import numpy as np
from sklearn.linear_model import LinearRegression

rng = np.random.default_rng(0)
dien_tich = rng.uniform(30, 120, 40)                              # m²
gia = 0.045 * dien_tich + 0.5 + rng.normal(0, 0.35, 40)           # tỉ đồng (có nhiễu)

# Chuẩn hoá đầu vào giúp gradient descent hội tụ nhanh
x = (dien_tich - dien_tich.mean()) / dien_tich.std()
w, b = 0.0, 0.0                                                   # mô hình: gia ≈ w*x + b
toc_do_hoc = 0.1
for vong in range(201):
    du_doan = w * x + b
    sai = du_doan - gia
    mse = (sai ** 2).mean()                                       # hàm mất mát: sai số bình phương trung bình
    dw = 2 * (sai * x).mean()                                     # đạo hàm của MSE theo w
    db = 2 * sai.mean()                                           # đạo hàm theo b
    w -= toc_do_hoc * dw                                          # bước xuống dốc
    b -= toc_do_hoc * db
    if vong in (0, 5, 20, 50, 200):
        print(f"vòng {vong:>3}: MSE = {mse:.4f}  w = {w:.4f}  b = {b:.4f}")

# Quy đổi về đơn vị gốc: gia = a * dien_tich + c
a = w / dien_tich.std()
c = b - a * dien_tich.mean()
print(f"\nMô hình tự học : giá = {a:.4f} x diện tích + {c:.3f}")

mo_hinh = LinearRegression().fit(dien_tich.reshape(-1, 1), gia)
print(f"scikit-learn   : giá = {mo_hinh.coef_[0]:.4f} x diện tích + {mo_hinh.intercept_:.3f}")
print(f"R² (độ khớp, 1 là tuyệt đối): {mo_hinh.score(dien_tich.reshape(-1, 1), gia):.3f}")

for s in (50, 80, 100):
    print(f"  Nhà {s} m² -> dự đoán {a * s + c:.2f} tỉ đồng")
