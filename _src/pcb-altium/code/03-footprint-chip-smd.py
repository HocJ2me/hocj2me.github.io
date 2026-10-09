"""Tính land pattern (pad) cho điện trở / tụ dán (chip) – theo ý tưởng IPC-7351 (rút gọn, dùng kích thước danh định)
   S (khe giữa 2 đầu cực) = L − 2·T
   Z (mép ngoài 2 pad) = L + 2·Jt + Cz        Jt: mối hàn mũi (toe)
   G (mép trong 2 pad) = S − 2·Jh − Cg        Jh: mối hàn gót (heel)
   X (rộng pad)        = W + 2·Js + Cx        Js: mối hàn cạnh (side)
   Mức B (nominal) cho chip >= 0603: Jt = 0.35, Jh = −0.05, Js = 0.00 (mm)
   Cz, Cg, Cx: tổng dung sai = sqrt(dung_sai_linh_kien² + F² + P²), F = sai số chế tạo 0.05, P = sai số gắp đặt 0.05
Chạy: python 03-footprint-chip-smd.py"""
import math

JT, JH, JS = 0.35, -0.05, 0.00
F, P = 0.05, 0.05

# Kích thước linh kiện theo datasheet điện trở chip (mm): (L, ±L, W, ±W, T đầu cực, ±T)
LINH_KIEN = {
    "0402 (1005)": (1.00, 0.05, 0.50, 0.05, 0.25, 0.10),
    "0603 (1608)": (1.60, 0.10, 0.80, 0.10, 0.30, 0.20),
    "0805 (2012)": (2.00, 0.10, 1.25, 0.10, 0.40, 0.20),
    "1206 (3216)": (3.20, 0.10, 1.60, 0.10, 0.50, 0.25),
}


def land_pattern(L, dL, W, dW, T, dT):
    S = L - 2 * T
    Cz = math.sqrt(dL ** 2 + F ** 2 + P ** 2)
    Cg = math.sqrt(dL ** 2 + (2 * dT) ** 2 + F ** 2 + P ** 2) / 2
    Cx = math.sqrt(dW ** 2 + F ** 2 + P ** 2)
    Z = L + 2 * JT + Cz
    G = S - 2 * JH - Cg
    X = W + 2 * JS + Cx
    return Z, G, X, (Z - G) / 2, (Z + G) / 2


print(f"{'Gói':<12}| {'Z':>5} | {'G':>5} | {'pad dài x rộng':>15} | {'tâm–tâm':>7}")
print("-" * 56)
for ten, kt in LINH_KIEN.items():
    Z, G, X, l, c = land_pattern(*kt)
    print(f"{ten:<12}| {Z:>5.2f} | {G:>5.2f} | {l:>6.2f} x {X:<6.2f} | {c:>7.2f}")

print("\nGhi chú: làm tròn tới 0.05 mm khi nhập vào Altium; courtyard = Z và X cộng thêm 0.25 mm mỗi phía.")
Z, G, X, l, c = land_pattern(*LINH_KIEN["0603 (1608)"])
print(f"Ví dụ 0603 nhập vào Altium: 2 pad {round(l / .05) * .05:.2f} x {round(X / .05) * .05:.2f} mm, "
      f"tâm pad tại x = ±{c / 2:.3f} mm, courtyard {Z + 0.5:.2f} x {X + 0.5:.2f} mm")
