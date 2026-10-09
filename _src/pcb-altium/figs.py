# -*- coding: utf-8 -*-
"""Hình minh hoạ cho khóa Thiết kế mạch PCB (Altium)."""
import math
from svg import svg, box, text, arrow, path

CU = 'class="cu"'


def design_flow():
    steps = [("Ý tưởng & sơ đồ khối", "bx-g"), ("Thư viện\nsymbol + footprint", "bx-c"), ("Mạch nguyên lý\n(.SchDoc)", "bx-a"),
             ("Kiểm tra ERC\n& BOM", "bx-a"), ("Layout PCB\n(.PcbDoc)", "bx-b"), ("Kiểm tra DRC", "bx-b"),
             ("Xuất Gerber,\nNC Drill, P&P", "bx-d"), ("Gia công\n& lắp ráp", "bx-d")]
    b = []
    for i, (t, c) in enumerate(steps):
        col, row = i % 4, i // 4
        x = 10 + col * 180 if row == 0 else 10 + (3 - col) * 180
        y = 14 + row * 92
        b.append(box(x, y, 150, 56, c, rx=8))
        for k, line in enumerate(t.split("\n")):
            b.append(text(x + 75, y + 25 + k * 16 - (8 if "\n" in t else 0), line, "s", "middle"))
        if i % 4 != 3:
            if row == 0: b.append(arrow(x + 150, y + 28, x + 178, y + 28))
            else:        b.append(arrow(x, y + 28, x - 28, y + 28))
    b.append(arrow(625, 70, 625, 104))
    b.append(text(10, 200, "Sai ở bước nào → quay lại sửa: lỗi DRC thường phải sửa từ footprint hoặc nguyên lý.", "xs mute"))
    return svg(730, 210, "".join(b), "Quy trình thiết kế PCB")


def cross_section(four=False):
    layers = ([("Silkscreen (chữ, ký hiệu)", "#f8fafc", 16), ("Solder mask (sơn phủ xanh)", "#16a34a", 16), ("Đồng TOP 35 µm", "#d97706", 16),
               ("Lõi FR-4 ~1.5 mm", "#d9c99a", 70), ("Đồng BOTTOM 35 µm", "#d97706", 16), ("Solder mask", "#16a34a", 16), ("Silkscreen", "#f8fafc", 16)]
              if not four else
              [("Solder mask", "#16a34a", 16), ("L1 TOP – tín hiệu", "#d97706", 16), ("Prepreg 0.21 mm", "#e7dcb6", 24), ("L2 – GND liền mạch", "#2563eb", 16),
               ("Lõi FR-4 1.065 mm", "#d9c99a", 56), ("L3 – nguồn (3V3, 5V)", "#dc2626", 16), ("Prepreg 0.21 mm", "#e7dcb6", 24),
               ("L4 BOTTOM – tín hiệu", "#d97706", 16), ("Solder mask", "#16a34a", 16)])
    b = []
    y = 14
    for name, color, h in layers:
        b.append(f'<rect x="40" y="{y}" width="360" height="{h}" fill="{color}" stroke="#475569" stroke-width="0.6"/>')
        b.append(text(414, y + h / 2 + 4, name, "xs"))
        y += h
    # via xuyên lỗ
    b.append(f'<rect x="200" y="14" width="18" height="{y - 14}" fill="#fff" stroke="#475569"/>')
    b.append(f'<rect x="196" y="14" width="4" height="{y - 14}" fill="#d97706"/><rect x="218" y="14" width="4" height="{y - 14}" fill="#d97706"/>')
    b.append(text(209, y + 16, "via xuyên lỗ", "xs mute", "middle"))
    title = "Mặt cắt mạch 4 lớp 1.6 mm (stack-up chuẩn: SIG – GND – PWR – SIG)" if four else "Mặt cắt mạch 2 lớp 1.6 mm"
    b.append(text(40, y + 34, "(các lớp mỏng được vẽ phóng to để dễ nhìn, không đúng tỉ lệ)", "xs mute"))
    return svg(640, y + 44, "".join(b), title)


def via_types():
    b = []
    y0, h = 20, 110
    ys = [y0 + i * h / 4 for i in range(5)]
    for i in range(4):
        b.append(f'<rect x="20" y="{ys[i] + 2}" width="520" height="{h / 4 - 4}" fill="#e7dcb6" stroke="#cbd5e1"/>')
    for i, yy in enumerate(ys):
        b.append(f'<rect x="20" y="{yy - 2}" width="520" height="4" fill="#d97706"/>')
        b.append(text(548, yy + 4, f"L{i + 1}" if i < 4 else "", "xs mute"))
    vias = [("Through-hole", 60, 0, 4), ("Blind (mù)", 190, 0, 2), ("Buried (chôn)", 320, 1, 3), ("Micro-via", 450, 0, 1)]
    for name, x, a, z in vias:
        w = 12 if name != "Micro-via" else 8
        b.append(f'<rect x="{x}" y="{ys[a] - 2}" width="{w}" height="{ys[min(z, 4)] - ys[a] + 4 if z < 4 else ys[3] + h / 4 - ys[a] + 2}" fill="#d97706"/>')
        b.append(text(x + w / 2, y0 + h + 22, name, "s", "middle"))
    b.append(text(20, y0 + h + 44, "Mạch 2–4 lớp giá rẻ chỉ dùng via xuyên lỗ; blind/buried/micro-via cho mạch HDI (điện thoại, BGA).", "xs mute"))
    return svg(590, y0 + h + 54, "".join(b), "Các loại via")


def tht_pad():
    b = [f'<circle cx="150" cy="110" r="70" class="cu"/>', f'<circle cx="150" cy="110" r="40" fill="#fff" stroke="#475569"/>',
         f'<circle cx="150" cy="110" r="26" fill="#94a3b8"/>']
    b.append(arrow(150, 110, 176, 110))
    b.append(text(150, 104, "chân", "xs", "middle"))
    b.append(f'<line class="ln thin" x1="80" y1="200" x2="220" y2="200"/>')
    b.append(text(150, 216, "đường kính pad", "xs", "middle"))
    b.append(f'<line class="ln thin" x1="110" y1="185" x2="190" y2="185"/>')
    b.append(text(150, 180, "lỗ khoan", "xs", "middle"))
    b.append(f'<line class="ln thin" x1="190" y1="60" x2="220" y2="60"/>')
    b.append(text(232, 64, "vành khuyên (annular ring)", "xs"))
    lines = ["Lỗ khoan = chân lớn nhất + 0.2 mm", "Pad = lỗ + 2 × vành khuyên (≥ 0.3 mm khi hàn tay)",
             "Chân vuông/chữ nhật: dùng đường chéo", "Làm tròn lên kích thước mũi khoan có sẵn", "Pad số 1 vẽ hình VUÔNG để nhận biết chiều"]
    for i, l in enumerate(lines):
        b.append(text(300, 100 + i * 20, "• " + l, "s"))
    return svg(640, 226, "".join(b), "Pad linh kiện chân xuyên")


def smd_land():
    b = [text(10, 18, "Land pattern IPC-7351 cho linh kiện chip (nhìn từ trên xuống)", "s")]
    b.append(f'<rect x="90" y="50" width="120" height="90" class="cu"/><rect x="390" y="50" width="120" height="90" class="cu"/>')
    b.append(f'<rect x="160" y="70" width="280" height="50" fill="#475569" opacity="0.85"/>')
    b.append(f'<rect x="160" y="70" width="60" height="50" fill="#cbd5e1"/><rect x="380" y="70" width="60" height="50" fill="#cbd5e1"/>')
    b.append(text(300, 100, "thân linh kiện", "xs", "middle").replace('class="xs"', 'class="xs" style="fill:#fff"'))
    def dim(x1, x2, y, label):
        return (f'<line class="ln thin" x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" marker-start="url(#MARK)" marker-end="url(#MARK)"/>' + text((x1 + x2) / 2, y - 5, label, "xs", "middle"))
    b.append(dim(90, 510, 168, "Z – mép ngoài 2 pad"))
    b.append(dim(210, 390, 40, "G – khe giữa 2 pad"))
    b.append(dim(160, 440, 192, "L – chiều dài linh kiện"))
    b.append(text(70, 100, "Jt", "s", "middle"))
    b.append(text(232, 136, "Jh", "s", "middle"))
    b.append(f'<line class="ln thin" x1="530" y1="50" x2="530" y2="140" marker-start="url(#MARK)" marker-end="url(#MARK)"/>')
    b.append(text(540, 100, "X", "s"))
    b.append(text(10, 222, "Jt (toe): mối hàn phía mũi ngoài · Jh (heel): mối hàn phía trong · Js (side): mối hàn hai bên cạnh", "xs mute"))
    return svg(600, 232, "".join(b), "Land pattern linh kiện dán")


def chip_sizes():
    pk = [("0402", 1.0, 0.5), ("0603", 1.6, 0.8), ("0805", 2.0, 1.25), ("1206", 3.2, 1.6), ("2512", 6.4, 3.2)]
    s = 40
    b, x = [], 20
    for n, L, W in pk:
        b.append(f'<rect x="{x}" y="{100 - W * s / 2}" width="{L * s}" height="{W * s}" fill="#334155"/>')
        b.append(f'<rect x="{x}" y="{100 - W * s / 2}" width="{L * s * 0.2}" height="{W * s}" fill="#cbd5e1"/>')
        b.append(f'<rect x="{x + L * s * 0.8}" y="{100 - W * s / 2}" width="{L * s * 0.2}" height="{W * s}" fill="#cbd5e1"/>')
        b.append(text(x + L * s / 2, 182, n, "t", "middle"))
        b.append(text(x + L * s / 2, 198, f"{L} x {W} mm", "xs mute", "middle"))
        x += L * s + 34
    b.append(text(20, 20, "Mã kích thước hệ inch (0603 = 0.06 x 0.03 inch); hệ mét viết là 1608 (1.6 x 0.8 mm). Tỉ lệ thật.", "xs mute"))
    return svg(x, 210, "".join(b), "Kích thước linh kiện chip")


def decoupling():
    b = [text(10, 18, "Tụ lọc nguồn 100 nF: SAI vs ĐÚNG", "s")]
    for k, (title, good) in enumerate([("SAI: tụ xa, vòng dòng lớn", False), ("ĐÚNG: tụ sát chân, via GND ngay cạnh", True)]):
        ox = 10 + k * 330
        b.append(box(ox + 100, 40, 90, 90, "bx-g", rx=4, text="IC", tcls="t"))
        b.append(text(ox + 112, 62, "VCC", "xs"))
        b.append(text(ox + 112, 124, "GND", "xs"))
        cx, cy = (ox + 30, 190) if not good else (ox + 210, 52)
        b.append(f'<rect x="{cx}" y="{cy}" width="34" height="16" fill="#334155"/>')
        b.append(text(cx + 17, cy + 30 if not good else cy - 4, "100nF", "xs", "middle"))
        if not good:
            b.append(f'<polyline points="{ox + 100},58 {ox + 47},58 {cx + 4},{cy}" fill="none" stroke="#d97706" stroke-width="3"/>')
            b.append(f'<polyline points="{ox + 100},120 {ox + 80},120 {ox + 80},210 {cx + 30},210" fill="none" stroke="#2563eb" stroke-width="3"/>')
            b.append(f'<polygon points="{ox + 47},58 {ox + 100},58 {ox + 100},120 {ox + 80},120 {ox + 80},206 {cx + 30},206 {cx + 4},{cy}" fill="#dc2626" opacity="0.15"/>')
            b.append(text(ox + 20, 236, "diện tích vòng lớn → cảm kháng lớn, nhiễu", "xs", "start"))
        else:
            b.append(f'<line x1="{ox + 190}" y1="58" x2="{cx}" y2="60" stroke="#d97706" stroke-width="3"/>')
            b.append(f'<circle cx="{cx + 44}" cy="60" r="5" fill="#2563eb"/>')
            b.append(text(cx + 54, 64, "via → GND", "xs"))
            b.append(text(ox + 100, 236, "vòng dòng nhỏ nhất", "xs", "start"))
        b.append(text(ox + 20, 254, title, "s"))
    return svg(670, 264, "".join(b), "Đặt tụ decoupling")


def return_path():
    b = [text(10, 18, "Dòng tín hiệu đi trên đường mạch, dòng HỒI chạy ngay bên dưới trên mặt GND", "s")]
    for k, (title, split) in enumerate([("Mặt GND liền: dòng hồi đi thẳng dưới đường mạch ✓", False), ("Mặt GND bị cắt: dòng hồi phải đi vòng → anten phát nhiễu ✗", True)]):
        oy = 34 + k * 120
        b.append(f'<rect x="20" y="{oy + 30}" width="560" height="50" fill="#bfdbfe" stroke="#2563eb"/>')
        if split:
            b.append(f'<rect x="290" y="{oy + 30}" width="20" height="50" fill="#fff"/>')
            b.append(path(f"M540,{oy + 55} L320,{oy + 55} C315,{oy + 95} 285,{oy + 95} 280,{oy + 55} L60,{oy + 55}", "ln dash"))
        else:
            b.append(path(f"M540,{oy + 55} L60,{oy + 55}", "ln dash"))
        b.append(f'<line x1="60" y1="{oy + 18}" x2="540" y2="{oy + 18}" stroke="#d97706" stroke-width="5"/>')
        b.append(text(20, oy + 12, title, "xs"))
    return svg(600, 280, "".join(b), "Đường hồi dòng")


def bottleneck():
    b = [text(10, 18, "“Đường ống nước”: dòng điện như nước — chỗ hẹp nhất quyết định lưu lượng", "s")]
    b.append(f'<path d="M20,50 L250,50 L280,78 L360,78 L390,50 L620,50 L620,130 L390,130 L360,102 L280,102 L250,130 L20,130 Z" class="cu"/>')
    b.append(text(320, 94, "thắt cổ chai 0.25 mm", "xs", "middle"))
    for x in (60, 140, 470, 560):
        b.append(arrow(x, 90, x + 40, 90))
    b.append(text(20, 160, "Đường 3 mm cho 5 A nhưng có đoạn 0.25 mm (đi qua giữa 2 chân IC) → đoạn hẹp nóng đỏ, có thể cháy đứt.", "xs mute"))
    b.append(text(20, 178, "Sửa: đi vòng, dùng polygon/đồng lớp khác + cụm via, hoặc đổi vị trí linh kiện cho đường thẳng và rộng.", "xs mute"))
    return svg(640, 188, "".join(b), "Lỗi thắt cổ chai")


def thermal_relief():
    b = []
    for k, (title, relief) in enumerate([("Nối liền (direct connect)", False), ("Thermal relief (4 nan)", True)]):
        ox = 20 + k * 280
        b.append(f'<rect x="{ox}" y="20" width="220" height="140" class="cu"/>')
        if relief:
            b.append(f'<circle cx="{ox + 110}" cy="90" r="40" fill="#166534"/>')
            for dx, dy, w, h in ((-6, -40, 12, 30), (-6, 10, 12, 30), (-40, -6, 30, 12), (10, -6, 30, 12)):
                b.append(f'<rect x="{ox + 110 + dx}" y="{90 + dy}" width="{w}" height="{h}" class="cu"/>')
        b.append(f'<circle cx="{ox + 110}" cy="90" r="22" class="cu" stroke="#7c2d12"/>')
        b.append(f'<circle cx="{ox + 110}" cy="90" r="9" fill="#fff"/>')
        b.append(text(ox + 110, 182, title, "s", "middle"))
    b.append(text(20, 204, "Thermal relief giúp hàn dễ (mặt đồng lớn không hút hết nhiệt mỏ hàn); chân dòng lớn thì nối liền hoặc nan rộng.", "xs mute"))
    return svg(580, 214, "".join(b), "Thermal relief")


def kelvin():
    b = [text(10, 18, "Đo dòng bằng điện trở shunt: kết nối Kelvin (4 dây)", "s")]
    b.append(f'<rect x="230" y="70" width="140" height="44" fill="#334155"/><rect x="230" y="70" width="22" height="44" fill="#cbd5e1"/><rect x="348" y="70" width="22" height="44" fill="#cbd5e1"/>')
    b.append(text(300, 96, "R shunt 10 mΩ", "xs", "middle").replace('class="xs"', 'class="xs" style="fill:#fff"'))
    b.append(f'<rect x="40" y="72" width="194" height="40" class="cu"/><rect x="366" y="72" width="194" height="40" class="cu"/>')
    b.append(text(80, 66, "dòng lớn vào", "xs"))
    b.append(text(470, 66, "dòng lớn ra", "xs"))
    b.append(f'<polyline points="241,114 241,170 280,170" fill="none" stroke="#2563eb" stroke-width="2.5"/>')
    b.append(f'<polyline points="359,114 359,170 320,170" fill="none" stroke="#2563eb" stroke-width="2.5"/>')
    b.append(box(270, 160, 60, 40, "bx-c", rx=4, text="INA180", tcls="xs"))
    b.append(text(10, 222, "Hai dây cảm biến (xanh) lấy áp NGAY TẠI hai đầu shunt, đi song song sát nhau tới bộ khuếch đại.", "xs mute"))
    return svg(600, 232, "".join(b), "Kết nối Kelvin")


def diff_pair():
    b = [text(10, 18, "Cặp vi sai (USB D+/D−): đi song song, khoảng cách đều, chiều dài bằng nhau", "s")]
    b.append(f'<polyline points="20,60 300,60 320,80 600,80" fill="none" stroke="#d97706" stroke-width="5"/>')
    b.append(f'<polyline points="20,74 296,74 316,94 420,94 430,104 440,94 450,104 460,94 470,104 480,94 600,94" fill="none" stroke="#d97706" stroke-width="5"/>')
    b.append(text(450, 124, "đoạn uốn bù chiều dài (tuning)", "xs", "middle"))
    b.append(text(20, 50, "D+", "xs"))
    b.append(text(20, 92, "D−", "xs"))
    rules = ["Quy tắc 3W: khoảng cách giữa 2 đường tín hiệu khác nhau ≥ 3 lần bề rộng đường → giảm xuyên âm",
             "Quy tắc 20H: mặt nguồn lùi vào so với mặt GND 20 lần độ dày điện môi → giảm bức xạ ở mép mạch",
             "Không đi tín hiệu tốc độ cao qua khe hở của mặt GND; hạn chế via; góc gãy 45°, không gãy 90°"]
    for i, r in enumerate(rules):
        b.append(text(20, 152 + i * 20, "• " + r, "xs"))
    return svg(620, 210, "".join(b), "Cặp vi sai")


def microstrip():
    b = [f'<rect x="40" y="110" width="400" height="14" fill="#2563eb"/>', f'<rect x="40" y="60" width="400" height="50" fill="#e7dcb6"/>',
         f'<rect x="200" y="50" width="80" height="10" fill="#d97706"/>']
    b.append(text(450, 121, "mặt GND (L2)", "xs"))
    b.append(text(450, 90, "điện môi εr, dày h", "xs"))
    b.append(text(240, 44, "w (rộng), t (dày)", "xs", "middle"))
    b.append(f'<line class="ln thin" x1="30" y1="60" x2="30" y2="110" marker-start="url(#MARK)" marker-end="url(#MARK)"/>')
    b.append(text(14, 90, "h", "s"))
    b.append(text(40, 150, "Z0 = 87/√(εr+1.41) · ln(5.98h / (0.8w + t))", "mono"))
    b.append(text(40, 170, "Mạch 4 lớp, h = 0.21 mm, εr = 4.4: w ≈ 0.35 mm cho 50 Ω", "xs mute"))
    return svg(620, 180, "".join(b), "Microstrip")


def module_layout():
    b = [f'<rect x="20" y="20" width="420" height="240" fill="#166534" rx="8"/>']
    b.append(f'<rect x="140" y="20" width="180" height="70" fill="#fff" stroke="#dc2626" stroke-dasharray="6 4"/>')
    b.append(text(230, 50, "VÙNG CẤM ĐỒNG", "xs", "middle"))
    b.append(text(230, 66, "(antenna keep-out)", "xs", "middle"))
    b.append(box(150, 40, 160, 120, "bx-g", rx=4))
    b.append(text(230, 130, "ESP32-WROOM", "s", "middle"))
    b.append(f'<path d="M160,48 h20 v14 h20 v-14 h20 v14 h20 v-14 h20 v14 h20 v-14" fill="none" stroke="#d97706" stroke-width="3"/>')
    b.append(box(40, 190, 90, 50, "bx-b", rx=4, text="Nguồn", sub="LDO 3V3"))
    b.append(box(330, 180, 90, 60, "bx-c", rx=4, text="Driver", sub="động cơ"))
    b.append(box(190, 200, 80, 40, "bx-a", rx=4, text="USB-UART", tcls="xs"))
    lines = ["• Anten của module nhô ra MÉP mạch hoặc nằm trên vùng không có đồng ở mọi lớp",
             "• Phần công suất (driver động cơ) tách xa phần tín hiệu; GND nối tại 1 điểm hoặc qua mặt GND chung liền",
             "• Tụ 10 µF + 100 nF sát chân 3V3 của module (ESP32 kéo dòng đỉnh ~500 mA khi phát WiFi)"]
    for i, l in enumerate(lines):
        b.append(text(460, 60 + i * 0, "", "xs"))
        b.append(text(20, 284 + i * 18, l, "xs"))
    return svg(640, 336, "".join(b), "Bố trí mạch điều khiển ESP32")


def hbridge_loop():
    b = [text(10, 18, "Vòng dòng chuyển mạch của mạch cầu H: càng nhỏ càng ít nhiễu", "s")]
    b.append(box(40, 40, 80, 40, "bx-b", rx=4, text="Tụ bulk", tcls="xs"))
    b.append(box(200, 40, 80, 40, "bx-e", rx=4, text="MOSFET cao", tcls="xs"))
    b.append(box(200, 130, 80, 40, "bx-e", rx=4, text="MOSFET thấp", tcls="xs"))
    b.append(box(360, 85, 90, 40, "bx-c", rx=4, text="Động cơ", tcls="xs"))
    b.append(f'<polyline points="120,60 200,60" stroke="#d97706" stroke-width="4" fill="none"/><polyline points="240,80 240,130" stroke="#d97706" stroke-width="4" fill="none"/>')
    b.append(f'<polyline points="240,170 240,190 80,190 80,80" stroke="#2563eb" stroke-width="4" fill="none"/>')
    b.append(f'<polyline points="280,105 360,105" stroke="#d97706" stroke-width="4" fill="none"/>')
    b.append(f'<polygon points="120,60 200,60 240,80 240,190 80,190 80,80" fill="#dc2626" opacity="0.12"/>')
    b.append(text(150, 150, "vòng dòng di/dt cao", "xs", "middle"))
    b.append(text(20, 218, "Đặt tụ bulk + tụ gốm sát cặp MOSFET; đường nguồn và GND công suất", "xs mute"))
    b.append(text(20, 234, "rộng, ngắn, đi song song (hoặc chồng lên nhau ở 2 lớp).", "xs mute"))
    return svg(520, 244, "".join(b), "Vòng dòng mạch cầu H")


def trace_chart():
    """Đồ thị bề rộng đường theo dòng (IPC-2221, 1 oz, ΔT 10°C) – tính trực tiếp trong Python khi build."""
    def w(I, k):
        return (I / (k * 10 ** 0.44)) ** (1 / 0.725) / 1.378 * 0.0254
    x0, y0, W, H = 60, 20, 520, 220
    b = [f'<line class="ln" x1="{x0}" y1="{y0 + H}" x2="{x0 + W}" y2="{y0 + H}"/>', f'<line class="ln" x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0 + H}"/>']
    for I in range(0, 11, 2):
        b.append(text(x0 + I / 10 * W, y0 + H + 16, f"{I} A", "xs mute", "middle"))
    for mm in range(0, 9, 2):
        b.append(text(x0 - 8, y0 + H - mm / 8 * H + 4, f"{mm}", "xs mute", "end"))
        b.append(f'<line class="ln thin dash" x1="{x0}" y1="{y0 + H - mm / 8 * H}" x2="{x0 + W}" y2="{y0 + H - mm / 8 * H}"/>')
    for k, color, lbl in ((0.048, "#d97706", "lớp ngoài"), (0.024, "#2563eb", "lớp trong")):
        pts = " ".join(f"{x0 + I / 10 * W:.1f},{y0 + H - min(w(I, k), 8) / 8 * H:.1f}" for I in [i / 10 for i in range(1, 101)] if w(I, k) <= 8.2)
        b.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2.5"/>')
    b.append(text(x0 + W - 150, y0 + 150, "lớp ngoài (top/bottom)", "xs"))
    b.append(text(x0 + 140, y0 + 30, "lớp trong", "xs"))
    b.append(text(14, y0 + 10, "mm", "xs mute"))
    return svg(600, 270, "".join(b), "Bề rộng đường mạch theo dòng điện")
