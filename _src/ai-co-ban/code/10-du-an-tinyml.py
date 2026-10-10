"""Bài 10 – DỰ ÁN AI trên vi điều khiển (TinyML): nhận biết hoạt động (đứng yên / đi bộ / chạy / ngã)
từ cảm biến gia tốc MPU6050 gắn trên người. Huấn luyện trên máy tính -> xuất thành CODE C cho ESP32."""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

rng = np.random.default_rng(11)
NHAN = ["dung_yen", "di_bo", "chay", "nga"]


def tao_cua_so(loai):
    """Giả lập 1 giây dữ liệu (50 mẫu) độ lớn gia tốc |a| (đơn vị g)."""
    t = np.arange(50) / 50
    if loai == 0: a = 1 + rng.normal(0, 0.02, 50)
    elif loai == 1: a = 1 + 0.25 * np.sin(2 * np.pi * 2 * t + rng.uniform(0, 6)) + rng.normal(0, 0.05, 50)
    elif loai == 2: a = 1 + 0.8 * np.abs(np.sin(2 * np.pi * 3 * t + rng.uniform(0, 6))) + rng.normal(0, 0.1, 50)
    else:
        a = 1 + rng.normal(0, 0.05, 50)
        k = rng.integers(10, 35)
        a[k:k + 3] += rng.uniform(2.0, 3.0)          # cú va đập mạnh
        a[k + 3:] = rng.normal(0.95, 0.03, 50 - k - 3)
    return a


def dac_trung(a):                                    # rút gọn 50 mẫu thành 3 con số – tính được trên ESP32
    return [a.std(), a.max(), np.abs(np.diff(a)).mean()]


X, y = [], []
for loai in range(4):
    for _ in range(150):
        X.append(dac_trung(tao_cua_so(loai)))
        y.append(loai)
X, y = np.array(X), np.array(y)
X_hoc, X_thu, y_hoc, y_thu = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
cay = DecisionTreeClassifier(max_depth=3, random_state=0).fit(X_hoc, y_hoc)
print(f"Độ chính xác trên dữ liệu kiểm tra: {cay.score(X_thu, y_thu):.1%}")

# ----- Xuất cây quyết định thành hàm C (chạy được trên Arduino / ESP32, không cần thư viện AI) -----
TEN_DT = ["do_lech", "gia_tri_max", "bien_thien"]
t = cay.tree_


def sinh_c(nut, thut):
    pad = "    " * thut
    if t.children_left[nut] == -1:
        return f"{pad}return {int(np.argmax(t.value[nut]))};  // {NHAN[int(np.argmax(t.value[nut]))]}\n"
    s = f"{pad}if ({TEN_DT[t.feature[nut]]} <= {t.threshold[nut]:.4f}f) {{\n"
    s += sinh_c(t.children_left[nut], thut + 1)
    s += f"{pad}}} else {{\n" + sinh_c(t.children_right[nut], thut + 1) + f"{pad}}}\n"
    return s


print("\n// ===== Dán vào sketch ESP32 =====")
print("// 0 = đứng yên, 1 = đi bộ, 2 = chạy, 3 = NGÃ")
print("int nhanDangHoatDong(float do_lech, float gia_tri_max, float bien_thien) {")
print(sinh_c(0, 1), end="")
print("}")
print(f"// Kích thước mô hình: {t.node_count} nút – chỉ vài trăm byte Flash")
