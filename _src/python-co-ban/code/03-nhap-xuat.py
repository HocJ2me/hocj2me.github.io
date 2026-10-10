# Nhập dữ liệu với input() và in đẹp với f-string – ví dụ: tính chỉ số BMI

ten = input("Tên của bạn: ")
can_nang = float(input("Cân nặng (kg): "))       # input() luôn trả về CHUỖI -> phải ép sang số
chieu_cao = float(input("Chiều cao (m): "))

bmi = can_nang / chieu_cao ** 2

print()
print(f"Xin chào {ten}!")
print(f"Chỉ số BMI của bạn là {bmi:.1f}")         # :.1f -> 1 chữ số sau dấu phẩy
print(f"{'Cân nặng':<10}|{can_nang:>8.1f} kg")    # < căn trái, > căn phải, số là độ rộng
print(f"{'Chiều cao':<10}|{chieu_cao:>8.2f} m")
print(f"Tỉ lệ so với BMI 22: {bmi / 22:.0%}")       # :% -> phần trăm

# Nhiều giá trị trên một dòng
a, b = map(int, input("Nhập 2 số nguyên cách nhau dấu cách: ").split())
print(f"{a} + {b} = {a + b}, {a} x {b} = {a * b}")
