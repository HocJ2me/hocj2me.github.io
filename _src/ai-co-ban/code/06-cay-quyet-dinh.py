"""Bài 6 – Cây quyết định: mô hình "dễ hiểu" – in được ra các câu hỏi Có/Không như con người."""
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_text

# Dữ liệu tự tạo: có nên tưới cây không? [độ ẩm đất %, nhiệt độ °C, khả năng mưa %]
rng = np.random.default_rng(7)
do_am = rng.uniform(10, 90, 200)
nhiet = rng.uniform(18, 40, 200)
mua = rng.uniform(0, 100, 200)
X = np.column_stack([do_am, nhiet, mua])
# "Luật thật" (máy không biết): đất khô dưới 35% và sắp không mưa -> tưới; hoặc rất nóng và đất dưới 50%
y = (((do_am < 35) & (mua < 60)) | ((nhiet > 35) & (do_am < 50))).astype(int)

cay = DecisionTreeClassifier(max_depth=3, random_state=0).fit(X, y)
print(f"Độ chính xác trên dữ liệu học: {cay.score(X, y):.1%}")
print("Cây quyết định máy học được:\n")
print(export_text(cay, feature_names=["do_am", "nhiet_do", "kha_nang_mua"], class_names=["khong_tuoi", "TUOI"]))

print("Mức độ quan trọng của từng đặc trưng:")
for ten, qt in zip(["độ ẩm đất", "nhiệt độ", "khả năng mưa"], cay.feature_importances_):
    print(f"  {ten:<14}{'█' * int(qt * 40)} {qt:.2f}")

for mau in ([25, 30, 20], [25, 30, 80], [45, 38, 10], [70, 25, 0]):
    kq = cay.predict([mau])[0]
    print(f"  Đất {mau[0]}%, {mau[1]}°C, mưa {mau[2]}% -> {'TƯỚI' if kq else 'không tưới'}")
