# -*- coding: utf-8 -*-
"""Hình minh hoạ cho khóa C++ cơ bản."""
from svg import svg, box, text, arrow, path


def build_pipeline():
    steps = [("main.cpp", "mã nguồn", "bx-g"), ("Tiền xử lý", "#include, #define", "bx-a"),
             ("Biên dịch", "C++ → hợp ngữ", "bx-b"), ("Hợp dịch", "→ mã máy .o", "bx-c"),
             ("Liên kết", "ghép .o + thư viện", "bx-d"), (".exe / .elf / .hex", "file chạy được", "bx-g")]
    b = []
    for i, (t, s, c) in enumerate(steps):
        x = 10 + i * 128
        b.append(box(x, 30, 112, 56, c, text=t, sub=s, tcls="s"))
        if i:
            b.append(arrow(x - 14, 58, x - 2, 58))
    b.append(text(10, 18, "g++ main.cpp -o app", "mono"))
    b.append(text(10, 116, "Xem từng bước:  g++ -E (sau tiền xử lý)   g++ -S (ra hợp ngữ .s)   g++ -c (ra file .o)", "xs mute"))
    b.append(text(10, 136, "Với vi điều khiển: trình biên dịch chéo (arm-none-eabi-g++, xtensa-esp32-elf-g++) tạo .elf/.bin/.hex rồi nạp vào Flash.", "xs mute"))
    return svg(780, 146, "".join(b), "Quy trình build chương trình C++")


def type_sizes():
    rows = [("bool / char / int8_t / uint8_t", 1), ("short / int16_t / uint16_t", 2), ("int / float / int32_t / uint32_t", 4),
            ("double / long long / int64_t", 8)]
    b = []
    for i, (n, s) in enumerate(rows):
        y = 14 + i * 38
        b.append(text(10, y + 19, n, "s"))
        for k in range(s):
            b.append(box(260 + k * 56, y, 52, 28, "bx-a" if s < 4 else ("bx-b" if s == 4 else "bx-c"), rx=4, text="8 bit", tcls="xs"))
        b.append(text(260 + s * 56 + 8, y + 19, f"{s} byte", "xs mute"))
    return svg(780, 170, "".join(b), "Kích thước kiểu dữ liệu")


def memory_pointer():
    b = []
    cells = [("0x1000", "nhietDo", "35", "bx-a"), ("0x1004", "tocDo", "120", "bx"), ("0x1008", "p", "0x1000", "bx-b"), ("0x1010", "pp", "0x1008", "bx-c")]
    for i, (addr, name, val, c) in enumerate(cells):
        x = 30 + i * 175
        b.append(text(x + 60, 26, addr, "mono", "middle"))
        b.append(box(x, 34, 120, 44, c, text=val, tcls="t"))
        b.append(text(x + 60, 98, name, "s", "middle"))
    b.append(path("M440,106 C440,170 90,170 90,110", "ln"))
    b.append(text(265, 178, "p = &nhietDo  →  *p == 35", "xs mute", "middle"))
    b.append(path("M615,106 C615,150 445,150 445,110", "ln"))
    b.append(text(600, 150, "pp = &p  →  **pp == 35", "xs mute", "start"))
    return svg(760, 190, "".join(b), "Biến, địa chỉ và con trỏ trong bộ nhớ")


def array_memory():
    b = [text(10, 22, "int adc[5]  — các phần tử nằm LIỀN NHAU, mỗi phần tử 4 byte", "s")]
    for i, v in enumerate([100, 200, 300, 400, 500]):
        x = 20 + i * 110
        b.append(box(x, 40, 100, 40, "bx-a", rx=4, text=str(v), tcls="t"))
        b.append(text(x + 50, 98, f"adc[{i}]  /  *(pa+{i})", "mono", "middle"))
        b.append(text(x + 50, 118, f"0x{0x2000 + i * 4:04X}", "xs mute", "middle"))
    b.append(box(580, 40, 100, 40, "bx-e", rx=4, text="??? ", tcls="t"))
    b.append(text(630, 98, "adc[5]: NGOÀI mảng", "xs", "middle"))
    return svg(700, 130, "".join(b), "Mảng trong bộ nhớ")


def register_bits():
    b = [text(10, 20, "Thanh ghi PORTB (8 bit) – mỗi bit điều khiển một chân", "s")]
    vals = [0, 0, 1, 0, 0, 1, 0, 1]
    for i in range(8):
        bit = 7 - i
        x = 20 + i * 62
        b.append(text(x + 27, 44, f"bit {bit}", "xs mute", "middle"))
        b.append(box(x, 50, 54, 40, "bx-d" if vals[i] else "bx-g", rx=4, text=str(vals[i]), tcls="t"))
    ops = [("Đặt bit n", "REG |=  (1 << n)"), ("Xoá bit n", "REG &= ~(1 << n)"), ("Đảo bit n", "REG ^=  (1 << n)"), ("Đọc bit n", "(REG >> n) & 1")]
    for i, (t, c) in enumerate(ops):
        x = 20 + (i % 2) * 260
        y = 118 + (i // 2) * 28
        b.append(text(x, y, t, "s"))
        b.append(text(x + 90, y, c, "mono"))
    return svg(540, 172, "".join(b), "Thao tác bit trên thanh ghi")


def endian():
    b = [text(10, 20, "uint32_t so = 0x12345678 nằm trong bộ nhớ như thế nào?", "s")]
    for row, (name, order, cls) in enumerate([("Little endian (x86, ARM, ESP32)", ["78", "56", "34", "12"], "bx-a"),
                                              ("Big endian (mạng TCP/IP, một số MCU cũ)", ["12", "34", "56", "78"], "bx-b")]):
        y = 40 + row * 70
        b.append(text(10, y + 26, name, "s"))
        for i, v in enumerate(order):
            x = 310 + i * 70
            b.append(box(x, y, 62, 38, cls, rx=4, text=v, tcls="t"))
            if row == 0:
                b.append(text(x + 31, y - 6, f"+{i}", "xs mute", "middle"))
    return svg(600, 180, "".join(b), "Thứ tự byte little endian và big endian")


def memory_layout():
    segs = [("Stack ↓", "biến cục bộ, tham số hàm, địa chỉ trả về", "bx-a", 54), ("(vùng trống)", "stack và heap lớn dần về phía nhau", "bx-g", 40),
            ("Heap ↑", "new / malloc – cấp phát động", "bx-b", 54), (".bss / .data", "biến toàn cục, biến static", "bx-c", 46),
            (".text (Flash)", "mã lệnh, hằng số const", "bx-d", 46)]
    b = []
    y = 10
    for t, s, c, h in segs:
        b.append(box(20, y, 160, h, c, rx=2, text=t, tcls="s"))
        b.append(text(196, y + h / 2 + 4, s, "s"))
        y += h
    b.append(text(20, y + 22, "Arduino Uno: 2 KB RAM chứa cả stack + heap + biến toàn cục — chạm nhau là treo máy!", "xs mute"))
    return svg(560, y + 32, "".join(b), "Bố cục bộ nhớ chương trình")


def inheritance_tree():
    b = [box(230, 10, 170, 50, "bx-c", text="CamBien", sub="ten_, chan_ (protected)")]
    kids = [("CamBienNhiet", "docC()", 40), ("CamBienAnhSang", "troiToi()", 240), ("CamBienKhoangCach", "docCm()", 440)]
    for n, m, x in kids:
        b.append(box(x, 120, 170, 50, "bx-a", text=n, sub=m))
        b.append(f'<polyline class="ln" points="{x + 85},120 {x + 85},92 315,92 315,64"/>')
    b.append('<polygon points="315,60 308,73 322,73" fill="#fff" stroke="#475569" stroke-width="1.5"/>')
    b.append(text(315, 192, "Lớp con KẾ THỪA mọi thứ của lớp cha và bổ sung chức năng riêng (quan hệ \"là một\")", "xs mute", "middle"))
    return svg(640, 200, "".join(b), "Cây kế thừa")


def vtable():
    b = []
    objs = [("DongCoDC", "vtable DongCoDC", ["~DongCoDC()", "DongCoDC::chay()"]), ("Servo", "vtable Servo", ["~Servo()", "Servo::chay()"])]
    for i, (o, vt, fns) in enumerate(objs):
        y = 20 + i * 100
        b.append(box(20, y, 140, 60, "bx-a", rx=6, text=f"đối tượng {o}", sub="vptr | dữ liệu..."))
        b.append(arrow(160, y + 30, 248, y + 30))
        b.append(box(250, y, 170, 60, "bx-b", rx=6))
        b.append(text(335, y + 18, vt, "s", "middle"))
        for k, f in enumerate(fns):
            b.append(text(262, y + 36 + k * 16, f"[{k}] {f}", "mono"))
    b.append(text(460, 50, "p->chay(128):", "mono"))
    b.append(text(460, 70, "1. đọc vptr trong đối tượng", "xs mute"))
    b.append(text(460, 88, "2. tra ô [1] trong vtable", "xs mute"))
    b.append(text(460, 106, "3. gọi hàm tìm được", "xs mute"))
    b.append(text(460, 136, "→ hàm đúng với KIỂU THẬT", "s"))
    return svg(700, 200, "".join(b), "Bảng hàm ảo vtable")


def race_timeline():
    b = [text(10, 18, "Hai luồng cùng làm dem++ (gồm 3 bước: đọc → cộng → ghi) mà không khoá:", "s")]
    t1 = [("đọc dem=5", 20), ("cộng → 6", 150), ("ghi dem=6", 380)]
    t2 = [("đọc dem=5", 90), ("cộng → 6", 250), ("ghi dem=6", 470)]
    b.append(text(10, 52, "Luồng A", "s"))
    b.append(text(10, 102, "Luồng B", "s"))
    for t, x in t1:
        b.append(box(80 + x, 34, 100, 28, "bx-a", rx=4, text=t, tcls="xs"))
    for t, x in t2:
        b.append(box(80 + x, 84, 100, 28, "bx-b", rx=4, text=t, tcls="xs"))
    b.append(arrow(80, 132, 680, 132, label="thời gian", lx=640, ly=126))
    b.append(text(10, 158, "Kết quả: dem = 6 thay vì 7 — một lần cộng bị MẤT. Giải pháp: mutex hoặc std::atomic.", "s"))
    return svg(700, 170, "".join(b), "Data race giữa hai luồng")


def ring_buffer():
    import math
    b = []
    cx, cy, r = 130, 110, 80
    vals = ["510", "520", "530", "", "", "", "", "500"]
    for i in range(8):
        a0 = -math.pi / 2 + i * 2 * math.pi / 8
        x, y = cx + r * math.cos(a0), cy + r * math.sin(a0)
        cls = "bx-a" if vals[i] else "bx-g"
        b.append(f'<circle class="{cls}" cx="{x:.0f}" cy="{y:.0f}" r="22"/>')
        b.append(text(x, y + 4, vals[i] or "–", "xs", "middle"))
        b.append(text(cx + (r + 36) * math.cos(a0), cy + (r + 36) * math.sin(a0) + 4, f"[{i}]", "xs mute", "middle"))
    b.append(text(cx, cy - 4, "N = 8", "s", "middle"))
    b.append(text(cx, cy + 14, "đếm = 4", "xs mute", "middle"))
    b.append(text(280, 50, "• dau (đọc ra) đang ở [7], duoi (ghi vào) ở [3]", "s"))
    b.append(text(280, 76, "• Ghi:  buf[duoi] = v;  duoi = (duoi + 1) % N", "mono"))
    b.append(text(280, 100, "• Đọc:  v = buf[dau];  dau = (dau + 1) % N", "mono"))
    b.append(text(280, 130, "• Tới cuối mảng thì quay về đầu → không bao giờ", "s"))
    b.append(text(292, 148, "phải dịch chuyển dữ liệu, không cấp phát động.", "s"))
    b.append(text(280, 178, "Dùng cho: bộ đệm UART, lọc trung bình trượt, hàng đợi lệnh.", "xs mute"))
    return svg(640, 222, "".join(b), "Bộ đệm vòng")


def millis_timeline():
    b = [text(10, 18, "delay(500) chặn cả chương trình  vs  millis() không chặn", "s")]
    b.append(text(10, 52, "delay()", "s"))
    b.append(box(90, 36, 90, 26, "bx-d", rx=4, text="LED", tcls="xs"))
    b.append(box(180, 36, 260, 26, "bx-e", rx=4, text="delay(500): KHÔNG làm gì được", tcls="xs"))
    b.append(box(440, 36, 90, 26, "bx-d", rx=4, text="LED", tcls="xs"))
    b.append(text(10, 102, "millis()", "s"))
    for i in range(11):
        x = 90 + i * 40
        cls = "bx-d" if i in (0, 5, 10) else "bx-a"
        b.append(box(x, 86, 36, 26, cls, rx=4, text="LED" if i in (0, 5, 10) else "đọc", tcls="xs"))
    b.append(text(90, 136, "Mỗi vòng loop() vẫn đọc nút, cảm biến; chỉ đổi LED khi now − lanCuoi ≥ 500.", "xs mute"))
    return svg(560, 146, "".join(b), "So sánh delay và millis")


def flow_if():
    b = [box(200, 6, 160, 34, "bx-g", text="đọc nhiệt độ t"), arrow(280, 40, 280, 58)]
    b.append(f'<polygon class="bx-b" points="280,58 360,86 280,114 200,86"/>')
    b.append(text(280, 90, "t < 18 ?", "s", "middle"))
    b.append(arrow(360, 86, 430, 86, label="đúng"))
    b.append(box(432, 70, 120, 32, "bx-a", text="bật sưởi"))
    b.append(arrow(280, 114, 280, 136, label="sai", lx=300, ly=128))
    b.append(f'<polygon class="bx-b" points="280,136 360,164 280,192 200,164"/>')
    b.append(text(280, 168, "t ≤ 28 ?", "s", "middle"))
    b.append(arrow(360, 164, 430, 164, label="đúng"))
    b.append(box(432, 148, 120, 32, "bx-a", text="tắt hết"))
    b.append(arrow(280, 192, 280, 214, label="sai", lx=300, ly=206))
    b.append(box(220, 214, 120, 32, "bx-a", text="bật quạt"))
    return svg(580, 254, "".join(b), "Lưu đồ if else")


def oop_class():
    b = [box(20, 10, 240, 160, "bx", rx=8)]
    b.append(f'<rect class="bx-c" x="20" y="10" width="240" height="30" rx="8"/>')
    b.append(text(140, 30, "class Led", "t", "middle"))
    b.append(text(32, 60, "private:", "xs mute"))
    for i, s in enumerate(["const int pin_", "bool trangThai_", "int doSang_"]):
        b.append(text(44, 78 + i * 16, s, "mono"))
    b.append(text(32, 132, "public:", "xs mute"))
    b.append(text(44, 150, "bat()  tat()  datDoSang(v)", "mono"))
    b.append(arrow(260, 90, 330, 60))
    b.append(text(268, 118, "tạo ra", "xs mute"))
    for i, (n, p) in enumerate([("ledDo", "pin_=13, BẬT, 255"), ("ledXanh", "pin_=12, BẬT, 80")]):
        b.append(box(334, 20 + i * 76, 220, 56, "bx-a", text=f"đối tượng {n}", sub=p))
    b.append(text(20, 194, "Lớp = bản thiết kế.  Đối tượng = sản phẩm cụ thể làm từ bản thiết kế, mỗi cái có dữ liệu riêng.", "xs mute"))
    return svg(580, 204, "".join(b), "Lớp và đối tượng")


def stl_containers():
    items = [("vector", "mảng động, truy cập [i] nhanh", "bx-a"), ("array", "mảng cố định, không heap", "bx-a"),
             ("map", "khoá → giá trị, có thứ tự", "bx-b"), ("unordered_map", "khoá → giá trị, tra cực nhanh", "bx-b"),
             ("set", "tập không trùng, có thứ tự", "bx-c"), ("queue / stack", "FIFO / LIFO", "bx-d"),
             ("priority_queue", "lấy phần tử lớn nhất trước", "bx-d"), ("string", "chuỗi ký tự", "bx-g")]
    b = []
    for i, (n, s, c) in enumerate(items):
        x = 10 + (i % 4) * 172
        y = 10 + (i // 4) * 70
        b.append(box(x, y, 162, 58, c, text=n, sub=s, tcls="t"))
    return svg(700, 150, "".join(b), "Các container STL")
