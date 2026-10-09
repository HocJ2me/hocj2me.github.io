"""Tính trở kháng đặc tính của đường microstrip (đường trên lớp ngoài, có mặt GND ngay lớp dưới)
   Công thức IPC-2141:  Z0 = 87 / sqrt(εr + 1.41) · ln( 5.98·h / (0.8·w + t) )      (hợp lệ khi 0.1 < w/h < 2)
   Cặp vi sai (gần đúng): Zdiff ≈ 2·Z0·(1 − 0.48·e^(−0.96·s/h))
   Stack-up mẫu: mạch 4 lớp 1.6 mm, lớp prepreg 7628 dày h = 0.21 mm, εr ≈ 4.4, đồng ngoài 1 oz (t = 0.035 mm)
Chạy: python 04-tro-khang-microstrip.py"""
import math

H, ER, T = 0.21, 4.4, 0.035


def z0(w, h=H, er=ER, t=T):
    return 87 / math.sqrt(er + 1.41) * math.log(5.98 * h / (0.8 * w + t))


def zdiff(w, s, h=H):
    return 2 * z0(w, h) * (1 - 0.48 * math.exp(-0.96 * s / h))


def tim_be_rong(muc_tieu, h=H):
    lo, hi = 0.02, 3 * h                     # Z0 giảm khi w tăng -> chia đôi
    for _ in range(60):
        mid = (lo + hi) / 2
        if z0(mid, h) > muc_tieu: lo = mid
        else: hi = mid
    return (lo + hi) / 2


print("Z0 theo bề rộng đường (h = 0.21 mm, εr = 4.4):")
for w in [0.15, 0.20, 0.30, 0.40, 0.50]:
    print(f"  w = {w:.2f} mm -> Z0 = {z0(w):5.1f} Ω")

w50 = tim_be_rong(50)
print(f"\nĐường 50 Ω (anten 2.4 GHz, RF): w ≈ {w50:.3f} mm")

print("\nCặp vi sai USB 2.0 (mục tiêu 90 Ω ± 10%):")
for w, s in [(0.15, 0.15), (0.20, 0.15), (0.25, 0.15), (0.25, 0.20)]:
    z = zdiff(w, s)
    print(f"  w = {w:.2f}, s = {s:.2f} mm -> Zdiff ≈ {z:5.1f} Ω {'✓' if 81 <= z <= 99 else ''}")

print("\nNếu là mạch 2 lớp 1.6 mm (h = 1.5 mm), đường 50 Ω phải rộng:",
      f"{tim_be_rong(50, 1.5):.2f} mm -> quá to, vì vậy RF/high-speed nên dùng mạch 4 lớp.")
