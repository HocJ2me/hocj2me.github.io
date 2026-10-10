"""Bài 5 – Đánh giá mô hình: chia dữ liệu, độ chính xác, ma trận nhầm lẫn, precision / recall,
và hiện tượng QUÁ KHỚP (overfitting)."""
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# Bài toán y tế: dự đoán khối u lành (1) hay ác tính (0) từ 30 chỉ số ảnh siêu âm
du_lieu = load_breast_cancer()
X, y = du_lieu.data, du_lieu.target
X_hoc, X_thu, y_hoc, y_thu = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
mo_hinh = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(X_hoc, y_hoc)
du_doan = mo_hinh.predict(X_thu)

print(f"Số mẫu học {len(X_hoc)}, kiểm tra {len(X_thu)}")
print(f"Độ chính xác (accuracy): {(du_doan == y_thu).mean():.1%}")
tn, fp, fn, tp = confusion_matrix(y_thu, du_doan, labels=[0, 1]).ravel()
print("Ma trận nhầm lẫn (hàng = thật, cột = dự đoán):")
print(f"               đoán ác tính  đoán lành")
print(f"  thật ác tính      {tn:>4}        {fp:>4}   <- {fp} ca ác tính bị bỏ sót (nguy hiểm!)")
print(f"  thật lành         {fn:>4}        {tp:>4}")
print(f"Precision (đoán 'lành' thì đúng bao nhiêu): {precision_score(y_thu, du_doan):.1%}")
print(f"Recall    (tìm ra được bao nhiêu ca lành) : {recall_score(y_thu, du_doan):.1%}")
print(f"Recall cho lớp ác tính (quan trọng nhất)  : {recall_score(y_thu, du_doan, pos_label=0):.1%}")

# ----- Quá khớp: mô hình đa thức bậc cao "học thuộc" dữ liệu -----
rng = np.random.default_rng(3)
x = np.sort(rng.uniform(0, 1, 15))
y_that = np.sin(2 * np.pi * x) + rng.normal(0, 0.2, 15)
x_moi = np.linspace(x.min(), x.max(), 50)            # điểm MỚI nằm giữa các điểm đã học
y_moi = np.sin(2 * np.pi * x_moi)
print("\nĐa thức bậc d khớp 15 điểm (sai số trên dữ liệu học / dữ liệu mới):")
for d in (1, 3, 9):
    he_so = np.polyfit(x, y_that, d)
    sai_hoc = np.mean((np.polyval(he_so, x) - y_that) ** 2)
    sai_moi = np.mean((np.polyval(he_so, x_moi) - y_moi) ** 2)
    nhan_xet = "chưa khớp (underfit)" if d == 1 else ("vừa đẹp" if d == 3 else "QUÁ KHỚP (overfit)")
    print(f"  bậc {d:>2}: học {sai_hoc:.3f} | mới {sai_moi:.3f}  -> {nhan_xet}")
