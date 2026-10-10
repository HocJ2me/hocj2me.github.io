# Biến, kiểu dữ liệu, ép kiểu và toán tử

# ----- Biến: tên gắn với một giá trị -----
ten = "An"                 # str  – chuỗi
tuoi = 12                  # int  – số nguyên
chieu_cao = 1.52           # float – số thực
la_hoc_sinh = True         # bool – đúng/sai

print(ten, tuoi, chieu_cao, la_hoc_sinh)
print(type(ten), type(tuoi), type(chieu_cao), type(la_hoc_sinh))

# Biến có thể đổi giá trị (và cả kiểu)
diem = 7
diem = diem + 1.5          # giờ là float
print("Điểm sau khi cộng:", diem)

# Gán nhiều biến cùng lúc, hoán đổi hai biến
a, b = 3, 5
a, b = b, a
print("Sau khi đổi: a =", a, ", b =", b)

# ----- Ép kiểu -----
so_chuoi = "25"
print("Chuỗi + chuỗi:", so_chuoi + so_chuoi)            # nối chuỗi: 2525
print("Số + số:", int(so_chuoi) + int(so_chuoi))        # 50
print("float('3.5') =", float("3.5"), "| str(10) + '%' =", str(10) + "%")
print("int(9.99) =", int(9.99), "(cắt phần lẻ) | round(9.99) =", round(9.99))
print("bool(0) =", bool(0), "| bool('') =", bool(""), "| bool('abc') =", bool("abc"))

# ----- Toán tử -----
x = 17
print("x // 5 =", x // 5, "| x % 5 =", x % 5, "| x ** 2 =", x ** 2)
x += 3                     # x = x + 3
x *= 2                     # x = x * 2
print("x sau += 3 rồi *= 2:", x)
print("So sánh: 3 < 5 < 7 là", 3 < 5 < 7, "| 'a' == 'A' là", "a" == "A")
print("Logic: True and False =", True and False, "| not True =", not True)

# ----- Số thực có sai số -----
print("0.1 + 0.2 =", 0.1 + 0.2)
print("Làm tròn 2 chữ số:", round(0.1 + 0.2, 2))
