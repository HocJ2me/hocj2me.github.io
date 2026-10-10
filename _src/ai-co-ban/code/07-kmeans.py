"""Bài 7 – Học KHÔNG giám sát: phân cụm k-means tự viết bằng numpy.
Dữ liệu: vị trí (km) của 90 nhà học sinh – tìm 3 điểm đặt trạm xe buýt đưa đón."""
import numpy as np

rng = np.random.default_rng(5)
tam_that = np.array([[2, 3], [8, 8], [9, 2]])
X = np.vstack([rng.normal(t, 1.0, (30, 2)) for t in tam_that])     # 3 khu dân cư (máy không biết)

k = 3
tam = X[rng.choice(len(X), k, replace=False)]                          # bước 0: chọn ngẫu nhiên 3 tâm
for vong in range(1, 20):
    kc = np.linalg.norm(X[:, None, :] - tam[None, :, :], axis=2)        # khoảng cách mọi điểm tới mọi tâm
    nhom = kc.argmin(axis=1)                                            # bước 1: gán điểm vào tâm gần nhất
    tam_moi = np.array([X[nhom == j].mean(axis=0) for j in range(k)])   # bước 2: dời tâm về trung bình nhóm
    dich = np.linalg.norm(tam_moi - tam)
    tam = tam_moi
    print(f"vòng {vong}: tâm dịch chuyển {dich:.3f} km")
    if dich < 1e-3:
        print("-> hội tụ!")
        break

print("\nVị trí 3 trạm xe buýt đề xuất:")
for j in np.argsort(tam[:, 0]):
    print(f"  Trạm tại ({tam[j, 0]:.2f}, {tam[j, 1]:.2f}) km – phục vụ {np.sum(nhom == j)} học sinh, "
          f"xa nhất {np.max(np.linalg.norm(X[nhom == j] - tam[j], axis=1)):.2f} km")
