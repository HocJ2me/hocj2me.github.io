"""Bài 4 – Phân loại với k láng giềng gần nhất (kNN): tự viết bằng numpy và so sánh với scikit-learn.
Dữ liệu: hoa Iris, dùng 2 đặc trưng chiều dài và chiều rộng cánh hoa, 3 loài."""
import numpy as np
from collections import Counter
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

iris = load_iris()
X = iris.data[:, 2:4]                       # chiều dài, chiều rộng cánh hoa (cm)
y = iris.target
TEN = iris.target_names
X_hoc, X_thu, y_hoc, y_thu = train_test_split(X, y, test_size=0.3, random_state=1, stratify=y)
print(f"Dữ liệu học: {len(X_hoc)} bông, dữ liệu kiểm tra: {len(X_thu)} bông")


def knn_du_doan(x_moi, k=5):
    khoang_cach = np.sqrt(((X_hoc - x_moi) ** 2).sum(axis=1))   # khoảng cách Euclid tới MỌI mẫu học
    gan_nhat = np.argsort(khoang_cach)[:k]                        # chỉ số k mẫu gần nhất
    phieu = Counter(y_hoc[gan_nhat])                              # bỏ phiếu theo nhãn
    return phieu.most_common(1)[0][0]


for k in (1, 3, 5, 15):
    du_doan = np.array([knn_du_doan(x, k) for x in X_thu])
    print(f"k = {k:>2}: độ chính xác tự viết = {(du_doan == y_thu).mean():.1%}")

mo_hinh = KNeighborsClassifier(n_neighbors=5).fit(X_hoc, y_hoc)
print(f"scikit-learn (k = 5): {mo_hinh.score(X_thu, y_thu):.1%}")

for hoa in ([1.5, 0.3], [4.5, 1.4], [5.8, 2.2], [4.9, 1.7]):
    print(f"  Cánh {hoa[0]} x {hoa[1]} cm -> {TEN[knn_du_doan(np.array(hoa))]}")
