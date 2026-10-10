# Hàm: định nghĩa, tham số, giá trị trả về, phạm vi biến, lambda, đệ quy


def chao(ten):
    """Hàm in lời chào (dòng này là docstring – mô tả hàm)."""
    print(f"Xin chào {ten}!")


def dien_tich_hcn(dai, rong):
    return dai * rong                       # return trả kết quả về nơi gọi


def xep_loai(diem, nguong_gioi=8):         # tham số có giá trị mặc định
    return "Giỏi" if diem >= nguong_gioi else "Chưa giỏi"


def thong_ke(ds):
    return min(ds), max(ds), sum(ds) / len(ds)   # trả về nhiều giá trị (thực chất là tuple)


def tong_tat_ca(*cac_so):                  # nhận bao nhiêu số cũng được
    return sum(cac_so)


chao("Minh")
print("Diện tích 5 x 3 =", dien_tich_hcn(5, 3))
print("Gọi theo tên tham số:", dien_tich_hcn(rong=2, dai=10))
print(xep_loai(8.5), "|", xep_loai(8.5, nguong_gioi=9))
nho, lon, tb = thong_ke([7, 9, 5, 8])
print(f"min={nho}, max={lon}, tb={tb}")
print("tong_tat_ca(1, 2, 3, 4) =", tong_tat_ca(1, 2, 3, 4))

# ----- Phạm vi biến -----
dem = 0                                     # biến toàn cục


def tang():
    global dem                              # muốn sửa biến toàn cục phải khai báo global
    dem += 1


tang(); tang()
print("dem =", dem)

# ----- Hàm là giá trị: truyền hàm vào hàm khác, lambda -----
def ap_dung(f, x):
    return f(x)


print("ap_dung(abs, -5) =", ap_dung(abs, -5))
print("ap_dung(lambda x: x ** 3, 2) =", ap_dung(lambda x: x ** 3, 2))
ten = ["chi", "An", "bình"]
print("Sắp xếp không phân biệt hoa thường:", sorted(ten, key=lambda t: t.lower()))


# ----- Đệ quy -----
def giai_thua(n):
    return 1 if n <= 1 else n * giai_thua(n - 1)


def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


print("5! =", giai_thua(5), "| 10 số Fibonacci:", [fibonacci(i) for i in range(10)])
print("Docstring của chao:", chao.__doc__)
