# Dictionary (từ điển) và set (tập hợp)

# ----- dict: cặp khoá -> giá trị -----
hoc_sinh = {"ten": "An", "lop": "7A", "diem": 8.5}
print(hoc_sinh["ten"], "học lớp", hoc_sinh["lop"])
hoc_sinh["diem"] = 9                 # sửa
hoc_sinh["so_thich"] = "robot"       # thêm khoá mới
print(hoc_sinh)
print("Có khoá 'email'?", "email" in hoc_sinh, "| get với giá trị mặc định:", hoc_sinh.get("email", "chưa có"))

for khoa, gia_tri in hoc_sinh.items():
    print(f"  {khoa:<9}: {gia_tri}")

# Đếm tần suất từ – ứng dụng kinh điển của dict
van_ban = "học học nữa học mãi robot robot code"
dem = {}
for tu in van_ban.split():
    dem[tu] = dem.get(tu, 0) + 1
print("Tần suất:", dem)
pho_bien = max(dem, key=dem.get)
print("Từ xuất hiện nhiều nhất:", pho_bien, "-", dem[pho_bien], "lần")

# Danh sách các dict: bảng dữ liệu
lop = [
    {"ten": "An", "diem": 8.5},
    {"ten": "Bình", "diem": 6.0},
    {"ten": "Chi", "diem": 9.2},
]
lop.sort(key=lambda h: h["diem"], reverse=True)
print("Xếp hạng:", [h["ten"] for h in lop])

# Dict comprehension
binh_phuong = {x: x * x for x in range(1, 6)}
print("Bảng bình phương:", binh_phuong)

# ----- set: không trùng lặp, không thứ tự -----
mau = {"đỏ", "xanh", "đỏ", "vàng"}
print("Set tự bỏ trùng:", sorted(mau))
clb_robot = {"An", "Bình", "Chi", "Dũng"}
clb_tin = {"Chi", "Dũng", "Giang"}
print("Tham gia cả hai CLB:", sorted(clb_robot & clb_tin))
print("Tham gia ít nhất 1:", sorted(clb_robot | clb_tin))
print("Chỉ CLB robot:", sorted(clb_robot - clb_tin))
print("Lọc trùng trong list:", sorted(set([3, 1, 3, 2, 1])))
