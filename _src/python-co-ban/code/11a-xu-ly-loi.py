# Xử lý lỗi với try / except / else / finally và tự báo lỗi bằng raise

# Đọc thông báo lỗi (traceback) – lỗi KHÔNG được xử lý sẽ dừng chương trình:
#     ZeroDivisionError, ValueError, IndexError, KeyError, TypeError, FileNotFoundError...

def chia(a, b):
    try:
        kq = a / b
    except ZeroDivisionError:
        print(f"  Không chia {a} cho 0 được!")
        return None
    else:                                  # chạy khi KHÔNG có lỗi
        return kq
    finally:                               # luôn chạy (dọn dẹp)
        print(f"  (đã thử chia {a} / {b})")


print("10 / 4 =", chia(10, 4))
print("10 / 0 =", chia(10, 0))

# Nhập lại tới khi đúng – mẫu rất hay dùng
du_lieu_nhap = ["mười", "", "15"]            # giả lập người dùng gõ sai 2 lần
for chuoi in du_lieu_nhap:
    try:
        tuoi = int(chuoi)
        print("Tuổi hợp lệ:", tuoi)
        break
    except ValueError:
        print(f"'{chuoi}' không phải số, nhập lại!")

# Bắt nhiều loại lỗi
ds = [1, 2, 3]
tu_dien = {"a": 1}
for thu in ["ds[5]", "tu_dien['b']", "'5' + 5"]:
    try:
        eval(thu)
    except (IndexError, KeyError) as loi:
        print(f"{thu}: lỗi tra cứu -> {type(loi).__name__}: {loi}")
    except Exception as loi:
        print(f"{thu}: lỗi khác -> {type(loi).__name__}: {loi}")


# Tự báo lỗi khi dữ liệu không hợp lệ
def dat_toc_do(v):
    if not 0 <= v <= 255:
        raise ValueError(f"tốc độ phải trong 0..255, nhận được {v}")
    print("Đặt tốc độ động cơ:", v)


for v in (120, 300):
    try:
        dat_toc_do(v)
    except ValueError as loi:
        print("Bắt được lỗi:", loi)

print("\nLỗi không được bắt sẽ in traceback và dừng chương trình:")
int("abc")
print("Dòng này không bao giờ chạy")
