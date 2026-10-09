"""Via chịu được bao nhiêu dòng? – coi thân via mạ đồng như một đường mạch lớp TRONG (IPC-2221, k = 0.024)
   Tiết diện thành via = π · (d_lỗ + t) · t       t: độ dày lớp mạ (thường 20–25 µm)
Chạy: python 05-via-dong-dien.py"""
import math

MIL = 0.0254


def dong_qua_via(d_lo_mm, t_ma_mm=0.025, tang_nhiet=10):
    tiet_dien_mm2 = math.pi * (d_lo_mm + t_ma_mm) * t_ma_mm
    tiet_dien_mil2 = tiet_dien_mm2 / (MIL * MIL)
    return 0.024 * tang_nhiet ** 0.44 * tiet_dien_mil2 ** 0.725


print(f"{'Lỗ via (mm)':>11} | {'dòng tối đa (A)':>15}")
print("-" * 30)
for d in [0.2, 0.3, 0.4, 0.5, 0.6]:
    print(f"{d:>11.1f} | {dong_qua_via(d):>15.2f}")

I, d = 5, 0.3
n = math.ceil(I / dong_qua_via(d) * 1.25)           # +25% dự phòng
print(f"\nĐưa {I} A từ lớp TOP xuống lớp POWER bằng via {d} mm cần ít nhất {n} via (đã cộng 25% dự phòng).")
print("Mẹo: đặt các via thành cụm ngay sát pad, thay vì 1 via to ở xa.")
