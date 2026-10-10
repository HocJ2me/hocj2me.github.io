# -*- coding: utf-8 -*-
"""Hình minh hoạ cho khóa Python cơ bản."""
from svg import svg, box, text, arrow, path


def bien_hop():
    items = [("ten", '"An"', "str", "bx-a"), ("tuoi", "12", "int", "bx-b"), ("chieu_cao", "1.52", "float", "bx-c"), ("la_hoc_sinh", "True", "bool", "bx-d")]
    b = [text(10, 20, "Biến giống một chiếc hộp có NHÃN (tên biến) chứa một GIÁ TRỊ có KIỂU", "s")]
    for i, (n, v, k, c) in enumerate(items):
        x = 20 + i * 165
        b.append(box(x, 50, 140, 60, c, rx=10, text=v, tcls="t"))
        b.append(box(x + 20, 36, 100, 22, "bx", rx=11, text=n, tcls="xs"))
        b.append(text(x + 70, 130, f"kiểu {k}", "xs mute", "middle"))
    b.append(text(20, 160, "Gán lại: tuoi = tuoi + 1  → hộp “tuoi” giờ chứa 13 (giá trị cũ bị thay).", "xs mute"))
    return svg(690, 170, "".join(b), "Biến như chiếc hộp")


def list_chi_so():
    vals = [8, 6.5, 9, 7, 5.5]
    b = [text(10, 20, "diem = [8, 6.5, 9, 7, 5.5]", "mono")]
    for i, v in enumerate(vals):
        x = 40 + i * 100
        b.append(box(x, 40, 90, 46, "bx-a", rx=6, text=str(v), tcls="t"))
        b.append(text(x + 45, 104, f"diem[{i}]", "mono", "middle"))
        b.append(text(x + 45, 124, f"diem[{i - 5}]", "xs mute", "middle"))
    b.append(text(40, 150, "Chỉ số bắt đầu từ 0; chỉ số âm đếm từ cuối. Cắt lát diem[1:4] lấy phần tử 1, 2, 3 (không lấy 4).", "xs mute"))
    return svg(560, 160, "".join(b), "Chỉ số của list")


def dict_fig():
    pairs = [('"ten"', '"An"'), ('"lop"', '"7A"'), ('"diem"', "9")]
    b = [text(10, 20, "Dictionary: tra GIÁ TRỊ bằng KHOÁ, giống tra nghĩa bằng từ trong từ điển", "s")]
    for i, (k, v) in enumerate(pairs):
        y = 40 + i * 46
        b.append(box(30, y, 120, 34, "bx-b", rx=6, text=k, tcls="mono"))
        b.append(arrow(150, y + 17, 228, y + 17))
        b.append(box(230, y, 120, 34, "bx-a", rx=6, text=v, tcls="mono"))
    b.append(text(380, 70, 'hoc_sinh["diem"]  →  9', "mono"))
    b.append(text(380, 96, 'hoc_sinh.get("email", "?") → "?"', "mono"))
    return svg(640, 182, "".join(b), "Dictionary")


def vong_lap():
    b = [box(160, 6, 200, 34, "bx-g", text="tong = 0;  so = 1")]
    b.append(arrow(260, 40, 260, 60))
    b.append('<polygon class="bx-b" points="260,60 350,88 260,116 170,88"/>')
    b.append(text(260, 92, "so <= 100 ?", "s", "middle"))
    b.append(arrow(260, 116, 260, 140, label="đúng", lx=280, ly=132))
    b.append(box(180, 140, 160, 34, "bx-a", text="tong += so"))
    b.append(arrow(260, 174, 260, 194))
    b.append(box(180, 194, 160, 34, "bx-a", text="so += 1"))
    b.append(path("M180,211 L120,211 L120,88 L168,88"))
    b.append(text(70, 160, "quay lại", "xs mute"))
    b.append(arrow(350, 88, 430, 88, label="sai"))
    b.append(box(432, 72, 150, 32, "bx-d", text="in tong = 5050"))
    return svg(600, 238, "".join(b), "Lưu đồ vòng lặp")


def ham_may():
    b = [box(220, 40, 200, 80, "bx-c", rx=14, text="dien_tich_hcn", sub="return dai * rong", tcls="t")]
    b.append(text(60, 66, "dai = 5", "mono"))
    b.append(text(60, 94, "rong = 3", "mono"))
    b.append(arrow(140, 80, 218, 80, label="đầu vào (tham số)"))
    b.append(arrow(420, 80, 498, 80, label="đầu ra (return)"))
    b.append(text(510, 85, "15", "t"))
    b.append(text(20, 150, "Hàm như một cỗ máy: đưa nguyên liệu vào, nhận sản phẩm ra. Viết một lần, gọi lại nhiều lần.", "xs mute"))
    return svg(600, 160, "".join(b), "Hàm như cỗ máy")


def lop_doi_tuong():
    b = [box(20, 20, 230, 150, "bx", rx=8), '<rect class="bx-c" x="20" y="20" width="230" height="30" rx="8"/>', text(135, 40, "class HocSinh", "t", "middle")]
    for i, t in enumerate(["thuộc tính: ten, lop, diem", "phương thức: them_diem()", "                    diem_tb()"]):
        b.append(text(34, 74 + i * 22, t, "xs"))
    b.append(arrow(250, 80, 318, 50, label="tạo"))
    b.append(arrow(250, 110, 318, 140))
    b.append(box(320, 20, 230, 60, "bx-a", text='an = HocSinh("An", "7A")', sub="diem = [8, 9, 7.5]", tcls="mono"))
    b.append(box(320, 110, 230, 60, "bx-a", text='chi = HocSinh("Chi", "7B")', sub="diem = [10]", tcls="mono"))
    b.append(text(20, 196, "Lớp = khuôn bánh; đối tượng = từng chiếc bánh. Mỗi đối tượng có dữ liệu riêng nhưng dùng chung phương thức.", "xs mute"))
    return svg(570, 206, "".join(b), "Lớp và đối tượng")


def python_where():
    items = [("🌐 Web", "Django, Flask"), ("🤖 AI & dữ liệu", "numpy, pandas, scikit-learn"), ("🔌 Vi điều khiển", "MicroPython trên ESP32, Micro:bit"),
             ("🎮 Trò chơi", "pygame"), ("🔬 Khoa học", "matplotlib vẽ đồ thị"), ("⚙️ Tự động hoá", "xử lý file, Excel, gửi email")]
    b = []
    for i, (t, s) in enumerate(items):
        x = 10 + (i % 3) * 215
        y = 10 + (i // 3) * 70
        b.append(box(x, y, 200, 58, ["bx-a", "bx-b", "bx-c", "bx-d", "bx-e", "bx-g"][i], text=t, sub=s, tcls="t"))
    return svg(660, 150, "".join(b), "Python dùng ở đâu")
