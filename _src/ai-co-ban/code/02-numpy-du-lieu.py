"""Bài 2 – Dữ liệu và numpy: mảng, thống kê, chuẩn hoá, lọc."""
import numpy as np

# Nhiệt độ (°C) đo bởi trạm thời tiết trong 2 tuần, mỗi hàng 1 tuần, mỗi cột 1 ngày
nhiet = np.array([[29, 31, 30, 33, 34, 32, 28],
                  [27, 26, 30, 35, 36, 33, 31]])
print("Kích thước (shape):", nhiet.shape, "| số phần tử:", nhiet.size)
print("Trung bình cả 2 tuần:", nhiet.mean().round(2))
print("Trung bình mỗi tuần:", nhiet.mean(axis=1).round(2))
print("Nóng nhất mỗi ngày trong tuần:", nhiet.max(axis=0))
print("Độ lệch chuẩn:", nhiet.std().round(2))

# Phép toán trên CẢ mảng (không cần vòng lặp) – nhanh và gọn
do_f = nhiet * 9 / 5 + 32
print("Đổi sang °F (tuần 1):", do_f[0])

# Lọc bằng điều kiện
print("Các ngày trên 32°C:", nhiet[nhiet > 32])
print("Số ngày nóng:", (nhiet > 32).sum())

# Chuẩn hoá dữ liệu về 0..1 (min-max) – bước bắt buộc trước khi cho nhiều mô hình học
lo, hi = nhiet.min(), nhiet.max()
chuan_hoa = (nhiet - lo) / (hi - lo)
print("Chuẩn hoá min-max (tuần 1):", chuan_hoa[0].round(2))

# Chuẩn hoá z-score: trung bình 0, độ lệch chuẩn 1
z = (nhiet - nhiet.mean()) / nhiet.std()
print("z-score (tuần 2):", z[1].round(2))

# Dữ liệu có giá trị lỗi (cảm biến hỏng trả về -999) -> làm sạch
tho = np.array([28.5, 29.0, -999, 30.1, 29.8, -999, 31.2])
sach = tho[tho > -100]
print(f"Dữ liệu thô {len(tho)} mẫu, sau khi bỏ lỗi còn {len(sach)}, trung bình {sach.mean():.2f}")

# Ma trận ngẫu nhiên có seed – cho kết quả lặp lại được
rng = np.random.default_rng(42)
print("5 số ngẫu nhiên chuẩn:", rng.normal(0, 1, 5).round(3))
