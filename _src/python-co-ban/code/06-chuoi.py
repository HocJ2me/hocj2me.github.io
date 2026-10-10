# Chuỗi (string): chỉ số, cắt lát, phương thức xử lý

s = "Lập trình Python"
print("Độ dài:", len(s))
print("Ký tự đầu:", s[0], "| ký tự cuối:", s[-1])
print("Cắt lát s[0:8]:", s[0:8], "| s[-6:]:", s[-6:], "| đảo ngược:", s[::-1])

# Phương thức thường dùng
print(s.upper(), "|", s.lower(), "|", s.title())
print("Tìm 'Python' ở vị trí:", s.find("Python"), "| đếm 'n':", s.count("n"))
print("Thay thế:", s.replace("Python", "C++"))
print("Bắt đầu bằng 'Lập'?", s.startswith("Lập"), "| chứa 'trình'?", "trình" in s)

# Tách và ghép
cau = "  hôm nay   trời   đẹp  "
tu = cau.split()                          # tách theo khoảng trắng, bỏ khoảng trắng thừa
print("Các từ:", tu, "-> số từ:", len(tu))
print("Ghép lại:", "-".join(tu))
print("Bỏ khoảng trắng 2 đầu:", repr(cau.strip()))

# Duyệt từng ký tự: đếm nguyên âm
nguyen_am = 0
for ch in "Embedded Programming":
    if ch.lower() in "aeiou":
        nguyen_am += 1
print("Số nguyên âm trong 'Embedded Programming':", nguyen_am)

# Chuỗi không thể sửa trực tiếp (immutable)
ma = "abc"
# ma[0] = "x"   -> lỗi TypeError
ma = "x" + ma[1:]
print("Tạo chuỗi mới:", ma)

# Kiểm tra chuỗi đối xứng
for tu_kiem_tra in ["level", "python", "Radar"]:
    t = tu_kiem_tra.lower()
    print(f"'{tu_kiem_tra}' đối xứng? {t == t[::-1]}")

# Phân tích lệnh dạng "TEN:GIA_TRI" (giống dữ liệu gửi từ cảm biến)
du_lieu = "T:28.5;H:61;L:320"
for cap in du_lieu.split(";"):
    ten, gia_tri = cap.split(":")
    print(f"  {ten} = {float(gia_tri)}")
