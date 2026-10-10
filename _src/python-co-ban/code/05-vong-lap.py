# Vòng lặp for, while, break, continue – và trò chơi đoán số
import random

# ----- for với range(bắt_đầu, dừng_trước, bước) -----
print("Đếm:", end=" ")
for i in range(1, 6):
    print(i, end=" ")
print()
print("Số chẵn tới 10:", list(range(0, 11, 2)))
print("Đếm ngược:", list(range(5, 0, -1)))

# ----- Tính tổng bằng vòng lặp -----
tong = 0
for so in range(1, 101):
    tong += so
print("1 + 2 + ... + 100 =", tong)

# ----- Vòng lặp lồng nhau: bảng cửu chương 2..4 -----
for i in range(1, 4):
    print("  ".join(f"{b}x{i}={b * i:<2}" for b in range(2, 5)))

# ----- break và continue -----
for so in range(1, 20):
    if so % 3 == 0:
        continue             # bỏ qua số chia hết cho 3
    if so > 10:
        break                # dừng hẳn khi vượt 10
    print(so, end=" ")
print()

# ----- while + trò chơi đoán số -----
random.seed(7)               # cố định để ví dụ luôn ra cùng số bí mật
bi_mat = random.randint(1, 100)
so_lan = 0
while True:
    doan = int(input("Đoán số (1-100): "))
    so_lan += 1
    if doan < bi_mat:
        print("  -> lớn hơn nữa")
    elif doan > bi_mat:
        print("  -> nhỏ hơn")
    else:
        print(f"  -> ĐÚNG RỒI! Số bí mật là {bi_mat}, bạn đoán {so_lan} lần")
        break
