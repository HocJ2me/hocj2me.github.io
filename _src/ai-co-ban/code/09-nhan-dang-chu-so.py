"""Bài 9 – Nhận dạng chữ số viết tay (ảnh 8x8 điểm) bằng mạng nơ-ron MLP của scikit-learn."""
import numpy as np
from sklearn.datasets import load_digits
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

so = load_digits()                      # 1797 ảnh, mỗi ảnh 8x8 = 64 điểm ảnh, độ sáng 0..16
print(f"Số ảnh: {len(so.images)}, kích thước mỗi ảnh: {so.images[0].shape}")

KY_TU = " .:-=+*#%@"
def ve(anh):                            # in ảnh ra chữ để "nhìn" dữ liệu
    return ["".join(KY_TU[int(v / 16 * 9)] * 2 for v in hang) for hang in anh]

print("\nẢnh đầu tiên (nhãn = %d):" % so.target[0])
for dong in ve(so.images[0]):
    print("  " + dong)

X = so.data / 16.0                      # chuẩn hoá về 0..1
X_hoc, X_thu, y_hoc, y_thu = train_test_split(X, so.target, test_size=0.25, random_state=0, stratify=so.target)
mlp = MLPClassifier(hidden_layer_sizes=(64,), max_iter=400, random_state=0).fit(X_hoc, y_hoc)
print(f"\nMạng 64 -> 64 -> 10 nơ-ron, huấn luyện {mlp.n_iter_} vòng")
print(f"Độ chính xác trên {len(X_thu)} ảnh chưa từng thấy: {mlp.score(X_thu, y_thu):.1%}")

du_doan = mlp.predict(X_thu)
cm = confusion_matrix(y_thu, du_doan)
print("\nMa trận nhầm lẫn (hàng: số thật 0-9, cột: số dự đoán 0-9):")
for i, hang in enumerate(cm):
    print(f"  {i} | " + " ".join(f"{v:>2}" if v else " ." for v in hang))

sai = np.where(du_doan != y_thu)[0][:2]
for i in sai:
    print(f"\nẢnh bị nhận sai: thật là {y_thu[i]}, máy đoán {du_doan[i]}")
    for dong in ve(X_thu[i].reshape(8, 8) * 16):
        print("  " + dong)
