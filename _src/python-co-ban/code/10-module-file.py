# Module có sẵn (math, random, datetime, statistics) và đọc/ghi file
import math
import random
import statistics
from datetime import date, timedelta
import csv

# ----- math -----
print("math.pi =", round(math.pi, 5), "| sqrt(2) =", round(math.sqrt(2), 4), "| sin(30°) =", round(math.sin(math.radians(30)), 2))

# ----- random (seed để kết quả cố định) -----
random.seed(1)
print("Số ngẫu nhiên 1-6:", [random.randint(1, 6) for _ in range(5)])
print("Chọn ngẫu nhiên người trực nhật:", random.choice(["An", "Bình", "Chi", "Dũng"]))

# ----- datetime -----
ngay_thi = date(2026, 11, 15)
hom_nay = date(2026, 10, 10)
print(f"Còn {(ngay_thi - hom_nay).days} ngày tới ngày thi; 30 ngày nữa là {(hom_nay + timedelta(days=30)):%d/%m/%Y}")

# ----- Ghi file văn bản -----
with open("nhat_ky.txt", "w", encoding="utf-8") as f:      # with: tự đóng file khi xong
    f.write("Buổi 1: học print\n")
    f.write("Buổi 2: học biến\n")
with open("nhat_ky.txt", "a", encoding="utf-8") as f:      # "a": ghi thêm vào cuối
    f.write("Buổi 3: học vòng lặp\n")

with open("nhat_ky.txt", encoding="utf-8") as f:
    for i, dong in enumerate(f, 1):
        print(f"  dòng {i}: {dong.strip()}")

# ----- File CSV (mở được bằng Excel) -----
du_lieu = [("ten", "toan", "tin"), ("An", 8, 9), ("Bình", 6, 7), ("Chi", 9, 10)]
with open("diem.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(du_lieu)

with open("diem.csv", encoding="utf-8") as f:
    bang = list(csv.DictReader(f))
for h in bang:
    tb = (int(h["toan"]) + int(h["tin"])) / 2
    print(f"  {h['ten']}: trung bình {tb}")
print("Trung vị điểm Tin:", statistics.median(int(h["tin"]) for h in bang))
