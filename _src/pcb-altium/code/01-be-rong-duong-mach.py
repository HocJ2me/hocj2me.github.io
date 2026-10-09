"""Tính bề rộng đường mạch theo dòng điện – công thức IPC-2221
   I = k · ΔT^0.44 · A^0.725      (A: tiết diện, đơn vị mil²)
   k = 0.048 với lớp NGOÀI (top/bottom), 0.024 với lớp TRONG (khó toả nhiệt hơn)
Chạy: python 01-be-rong-duong-mach.py"""
import math

MIL = 0.0254            # 1 mil = 0.0254 mm
OZ_TO_MIL = 1.378       # 1 oz/ft² đồng ≈ 1.378 mil ≈ 35 µm
RHO_CU = 1.72e-8        # điện trở suất đồng (Ω·m) ở 20°C


def be_rong_mm(dong_A, tang_nhiet=10, oz=1.0, lop_ngoai=True):
    k = 0.048 if lop_ngoai else 0.024
    tiet_dien_mil2 = (dong_A / (k * tang_nhiet ** 0.44)) ** (1 / 0.725)
    return tiet_dien_mil2 / (oz * OZ_TO_MIL) * MIL


def sut_ap(dong_A, rong_mm, dai_mm, oz=1.0):
    day_m = oz * 35e-6
    R = RHO_CU * (dai_mm / 1000) / ((rong_mm / 1000) * day_m)
    return R, dong_A * R, dong_A ** 2 * R


print("Bề rộng tối thiểu (mm) cho phép tăng nhiệt ΔT = 10°C")
print(f"{'Dòng (A)':>9} | {'ngoài 1oz':>10} | {'ngoài 2oz':>10} | {'trong 1oz':>10}")
print("-" * 49)
for I in [0.3, 0.5, 1, 2, 3, 5, 10]:
    print(f"{I:>9} | {be_rong_mm(I):>10.2f} | {be_rong_mm(I, oz=2):>10.2f} | {be_rong_mm(I, lop_ngoai=False):>10.2f}")

print("\nẢnh hưởng của mức tăng nhiệt cho phép (2 A, lớp ngoài, 1 oz):")
for dT in [5, 10, 20, 30]:
    print(f"  ΔT = {dT:>2}°C -> {be_rong_mm(2, dT):.2f} mm")

print("\nSụt áp & công suất toả nhiệt trên đường dài 50 mm, 1 oz:")
for I, w in [(0.5, 0.25), (2, 0.8), (5, 2.5)]:
    R, V, P = sut_ap(I, w, 50)
    print(f"  {I} A, rộng {w} mm: R = {R * 1000:.1f} mΩ, sụt áp = {V * 1000:.0f} mV, P = {P * 1000:.0f} mW")
