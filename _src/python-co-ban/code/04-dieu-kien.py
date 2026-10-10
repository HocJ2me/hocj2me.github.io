# Câu lệnh điều kiện: if / elif / else, toán tử logic, match-case

diem = float(input("Nhập điểm trung bình: "))
if diem >= 8:
    xep_loai = "Giỏi"
elif diem >= 6.5:
    xep_loai = "Khá"
elif diem >= 5:
    xep_loai = "Trung bình"
else:
    xep_loai = "Yếu"
print(f"Điểm {diem} -> xếp loại {xep_loai}")

# Kết hợp điều kiện: năm nhuận chia hết cho 4 nhưng không chia hết cho 100, hoặc chia hết cho 400
nam = int(input("Nhập một năm: "))
nhuan = (nam % 4 == 0 and nam % 100 != 0) or nam % 400 == 0
print(f"Năm {nam} {'là' if nhuan else 'không là'} năm nhuận")    # biểu thức điều kiện một dòng

# Điều kiện lồng nhau
nhiet_do = 33
co_nguoi = True
if co_nguoi:
    if nhiet_do > 30:
        print("Có người và trời nóng -> bật quạt")
    else:
        print("Có người, trời mát -> tắt quạt")
else:
    print("Không có người -> tắt hết")

# match-case (Python 3.10+): chọn theo giá trị
lenh = input("Lệnh điều khiển robot (tien/lui/trai/phai): ").strip().lower()
match lenh:
    case "tien":
        print("Robot đi thẳng")
    case "lui":
        print("Robot đi lùi")
    case "trai" | "phai":
        print(f"Robot rẽ {lenh}")
    case _:
        print("Không hiểu lệnh")
