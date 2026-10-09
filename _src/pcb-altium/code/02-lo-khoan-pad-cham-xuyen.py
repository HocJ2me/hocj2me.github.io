"""Tính lỗ khoan và pad cho linh kiện CHÂN XUYÊN (THT) – theo khuyến nghị IPC-2222 / IPC-7251
   Lỗ khoan  = đường kính chân lớn nhất + khe hở (0.2 mm mức B; 0.25 mm mức A)
   Pad       = lỗ khoan + 2 x vành khuyên (annular ring, tối thiểu ~0.15–0.25 mm, nên >= 0.3 mm khi hàn tay)
   Chân hình chữ nhật: dùng đường chéo sqrt(a² + b²) làm "đường kính chân"
Chạy: python 02-lo-khoan-pad-cham-xuyen.py"""
import math

KHE_HO = 0.20           # mm
VANH_KHUYEN = 0.30      # mm – thoải mái cho hàn tay / xưởng giá rẻ
LO_CHUAN = [0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 2.0, 3.2]   # mũi khoan xưởng hay có (mm)


def tinh(ten, chan_mm=None, chan_cn=None):
    d = chan_mm if chan_mm else math.hypot(*chan_cn)
    lo_toi_thieu = d + KHE_HO
    lo = next(x for x in LO_CHUAN if x >= lo_toi_thieu - 1e-9)        # làm tròn lên mũi khoan có sẵn
    pad = lo + 2 * VANH_KHUYEN
    return ten, d, lo, pad


ds = [
    tinh("Điện trở 1/4W", chan_mm=0.6),
    tinh("LED 5 mm", chan_cn=(0.5, 0.5)),
    tinh("Header 2.54 mm", chan_cn=(0.64, 0.64)),
    tinh("IC DIP-8 (NE555)", chan_cn=(0.53, 0.25)),
    tinh("Tụ hoá 10x16", chan_mm=0.6),
    tinh("Diode 1N5408 (3A)", chan_mm=1.3),
    tinh("Transistor TO-220", chan_cn=(0.9, 0.5)),
    tinh("Domino KF301 (5.0)", chan_cn=(1.0, 0.8)),
]
print(f"{'Linh kiện':<22}| {'chân (mm)':>9} | {'lỗ khoan':>8} | {'pad':>5}")
print("-" * 54)
for ten, d, lo, pad in ds:
    print(f"{ten:<22}| {d:>9.2f} | {lo:>8.2f} | {pad:>5.2f}")

print("\nKiểm tra khoảng hở giữa 2 pad header 2.54 mm:")
pad_header = ds[2][3]
khe = 2.54 - pad_header
print(f"  pad {pad_header:.2f} mm -> khe giữa 2 pad = {khe:.2f} mm "
      f"({'đi được 1 đường 0.25 mm + 2 khe 0.2 mm' if khe >= 0.65 else 'KHÔNG đủ chỗ đi dây giữa 2 chân'})")
