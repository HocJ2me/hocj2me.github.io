# List (danh sách) và tuple

diem = [8, 6.5, 9, 7, 5.5]
print("Danh sách điểm:", diem)
print("Phần tử đầu:", diem[0], "| cuối:", diem[-1], "| 3 phần tử đầu:", diem[:3])
print("Số phần tử:", len(diem), "| tổng:", sum(diem), "| lớn nhất:", max(diem), "| nhỏ nhất:", min(diem))
print("Trung bình:", round(sum(diem) / len(diem), 2))

# Thêm / xoá / sửa
diem.append(10)            # thêm vào cuối
diem.insert(0, 4)          # chèn vào vị trí 0
diem[2] = 7.5              # sửa
diem.remove(5.5)           # xoá theo giá trị
cuoi = diem.pop()          # lấy ra phần tử cuối
print("Sau khi sửa:", diem, "| vừa lấy ra:", cuoi)

# Sắp xếp
print("sorted (tạo list mới):", sorted(diem))
diem.sort(reverse=True)    # sắp xếp tại chỗ, giảm dần
print("sort giảm dần:", diem)

# Duyệt kèm chỉ số
for i, d in enumerate(diem, start=1):
    print(f"  Bài {i}: {d}")

# List comprehension: tạo list nhanh
binh_phuong = [x * x for x in range(1, 8)]
diem_dat = [d for d in diem if d >= 5]
print("Bình phương:", binh_phuong)
print("Điểm đạt:", diem_dat)

# List lồng nhau (ma trận)
ma_tran = [[1, 2, 3], [4, 5, 6]]
print("Phần tử hàng 2 cột 3:", ma_tran[1][2])

# Cẩn thận: gán list là dùng CHUNG, muốn sao chép dùng .copy()
a = [1, 2, 3]
b = a
c = a.copy()
a.append(4)
print("a =", a, "| b (dùng chung) =", b, "| c (bản sao) =", c)

# Tuple: giống list nhưng KHÔNG sửa được – dùng cho dữ liệu cố định
toa_do = (21.0285, 105.8542)
vi_do, kinh_do = toa_do        # tách tuple
print(f"Hà Nội: vĩ độ {vi_do}, kinh độ {kinh_do}")
# toa_do[0] = 0   -> lỗi
