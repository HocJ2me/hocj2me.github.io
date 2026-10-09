"""Mạch đo dòng (điện trở shunt) và đo áp (cầu phân áp) cho ADC 12 bit của ESP32 (0–3.3 V)
Chạy: python 06-do-dong-do-ap.py"""

ADC_BIT, VREF = 12, 3.3
LSB = VREF / (2 ** ADC_BIT)

print("== ĐO ÁP: pin 24 V qua cầu phân áp R1 (trên) – R2 (dưới) ==")
V_MAX = 25.2                                   # pin 6S đầy 25.2 V
for R1, R2 in [(100e3, 10e3), (100e3, 15e3), (68e3, 10e3)]:
    he_so = R2 / (R1 + R2)
    v_adc = V_MAX * he_so
    dong_tieu_thu = V_MAX / (R1 + R2)
    ok = "VƯỢT 3.3 V – hỏng chân ADC!" if v_adc > VREF else ("sát 3.3 V, không còn dự phòng" if v_adc > 0.9 * VREF else "OK")
    print(f"  R1 = {R1 / 1e3:.0f}k, R2 = {R2 / 1e3:.0f}k: Vadc max = {v_adc:.2f} V ({ok}), "
          f"độ phân giải = {LSB / he_so * 1000:.1f} mV/bước, dòng rò = {dong_tieu_thu * 1e6:.0f} µA")

R_LOC, C_LOC = 10e3, 100e-9
import math
fc = 1 / (2 * math.pi * R_LOC * C_LOC)
print(f"  Lọc RC {R_LOC / 1e3:.0f}k + {C_LOC * 1e9:.0f}nF trước chân ADC: tần số cắt {fc:.0f} Hz")

print("\n== ĐO DÒNG: điện trở shunt + khuếch đại (INA180 gain 50) ==")
I_MAX, V_SHUNT_MAX = 5.0, 0.05                 # muốn sụt áp trên shunt <= 50 mV ở dòng max
R_SHUNT = V_SHUNT_MAX / I_MAX
GAIN = 50
P = I_MAX ** 2 * R_SHUNT
v_ra = I_MAX * R_SHUNT * GAIN
print(f"  R_shunt = {R_SHUNT * 1000:.0f} mΩ, công suất ở {I_MAX} A = {P:.2f} W -> chọn shunt 2512 loại 1 W")
print(f"  Điện áp ra khuếch đại ở {I_MAX} A = {v_ra:.2f} V (<= 3.3 V: OK)")
print(f"  Độ phân giải dòng = {LSB / (R_SHUNT * GAIN) * 1000:.1f} mA/bước ADC")
for I in [0.1, 1.0, 2.5]:
    adc = round(I * R_SHUNT * GAIN / LSB)
    print(f"  I = {I:>4} A -> giá trị ADC ≈ {adc}")
print("\nLayout: nối 2 dây cảm biến của bộ khuếch đại vào shunt theo kiểu KELVIN (4 dây),")
print("đi song song sát nhau tới chân IN+/IN−, không dùng chung đường dòng lớn.")
