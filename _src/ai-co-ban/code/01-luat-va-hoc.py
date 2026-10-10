"""Bài 1 – Lập trình truyền thống vs học máy.
Bài toán: từ chiều dài cánh hoa, đoán loài hoa diên vĩ (Iris versicolor hay virginica)."""
from sklearn.datasets import load_iris

iris = load_iris()
X = iris.data[50:, 2]            # chiều dài cánh hoa (cm) của 100 bông: 50 versicolor, 50 virginica
y = iris.target[50:] - 1         # 0 = versicolor, 1 = virginica
ten = ["versicolor", "virginica"]

# ----- Cách 1: LẬP TRÌNH TRUYỀN THỐNG – con người tự nghĩ ra luật -----
def luat_tu_viet(chieu_dai):
    return 1 if chieu_dai > 5.5 else 0        # "cảm giác" hoa virginica to hơn 5.5 cm


dung = sum(luat_tu_viet(x) == t for x, t in zip(X, y))
print(f"Luật tự viết (ngưỡng 5.5 cm): đúng {dung}/{len(y)}")

# ----- Cách 2: HỌC MÁY – máy tự tìm ngưỡng tốt nhất từ DỮ LIỆU -----
tot_nhat, nguong_tot = 0, None
for nguong in sorted(set(X)):                # thử mọi ngưỡng có thể
    so_dung = sum((1 if x > nguong else 0) == t for x, t in zip(X, y))
    if so_dung > tot_nhat:
        tot_nhat, nguong_tot = so_dung, nguong
print(f"Ngưỡng máy học được: {nguong_tot} cm -> đúng {tot_nhat}/{len(y)}")

# ----- Dùng "mô hình" vừa học để dự đoán hoa MỚI -----
for x_moi in [3.9, 4.8, 5.6]:
    print(f"  Cánh hoa {x_moi} cm -> đoán là {ten[int(x_moi > nguong_tot)]}")

print("\nThống kê dữ liệu (máy 'nhìn thấy' gì):")
for k in (0, 1):
    v = X[y == k]
    print(f"  {ten[k]:<10}: nhỏ nhất {v.min():.1f}, lớn nhất {v.max():.1f}, trung bình {v.mean():.2f} cm")
