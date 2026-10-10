# DỰ ÁN: Chương trình sổ điểm có menu – tổng hợp biến, điều kiện, vòng lặp, list, dict, hàm, file, xử lý lỗi
import json

FILE = "so_diem.json"
so_diem = {}                  # {tên: [điểm, điểm, ...]}


def tb(ds):
    return round(sum(ds) / len(ds), 2) if ds else 0


def them_hoc_sinh():
    ten = input("  Tên học sinh: ").strip()
    if not ten:
        print("  Tên không được trống")
    elif ten in so_diem:
        print("  Đã có học sinh này")
    else:
        so_diem[ten] = []
        print(f"  Đã thêm {ten}")


def nhap_diem():
    ten = input("  Tên: ").strip()
    if ten not in so_diem:
        print("  Không tìm thấy học sinh")
        return
    try:
        d = float(input("  Điểm: "))
        if not 0 <= d <= 10:
            raise ValueError
        so_diem[ten].append(d)
        print(f"  Đã ghi điểm {d} cho {ten}")
    except ValueError:
        print("  Điểm phải là số từ 0 đến 10")


def bang_xep_hang():
    print("  {:<4}{:<10}{:<18}{}".format("#", "Tên", "Các điểm", "TB"))
    xep = sorted(so_diem.items(), key=lambda kv: tb(kv[1]), reverse=True)
    for i, (ten, ds) in enumerate(xep, 1):
        print("  {:<4}{:<10}{:<18}{}".format(i, ten, ", ".join(map(str, ds)) or "-", tb(ds)))


def luu():
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(so_diem, f, ensure_ascii=False)
    print(f"  Đã lưu {len(so_diem)} học sinh vào {FILE}")


MENU = {"1": ("Thêm học sinh", them_hoc_sinh), "2": ("Nhập điểm", nhap_diem),
        "3": ("Bảng xếp hạng", bang_xep_hang), "4": ("Lưu file", luu)}

while True:
    print("\n== SỔ ĐIỂM ==  " + "  ".join(f"[{k}] {v[0]}" for k, v in MENU.items()) + "  [0] Thoát")
    chon = input("Chọn: ").strip()
    if chon == "0":
        print("Tạm biệt!")
        break
    if chon in MENU:
        MENU[chon][1]()
    else:
        print("  Lựa chọn không hợp lệ")
