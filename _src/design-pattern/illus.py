# -*- coding: utf-8 -*-
"""Hình minh hoạ vẽ tay (SVG) – dùng lớp CSS il-* định nghĩa trong trang."""


def _svg(w, h, body, label):
    return (f'<svg class="illus" viewBox="0 0 {w} {h}" style="max-width:{w}px" role="img" '
            f'aria-label="{label}" xmlns="http://www.w3.org/2000/svg">{body}</svg>')


def _arrow_defs(idp):
    return (f'<defs><marker id="{idp}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" class="il-arrowhead"/></marker></defs>')


def uml_legend():
    rows = [
        ("Kế thừa (extends)", "solid", "tri", "B là lớp con của A"),
        ("Cài đặt interface (implements)", "dash", "tri", "B cài đặt interface A"),
        ("Liên kết (association)", "solid", "open", "B giữ tham chiếu tới A"),
        ("Phụ thuộc (dependency)", "dash", "open", "B dùng / tạo ra A tạm thời"),
        ("Tập hợp (aggregation)", "solid", "dia", "A chứa B, B sống độc lập"),
        ("Hợp thành (composition)", "solid", "diaf", "A sở hữu B, huỷ A thì huỷ B"),
    ]
    out = []
    for i, (name, line, head, desc) in enumerate(rows):
        y = 26 + i * 40
        dash = ' stroke-dasharray="6 4"' if line == "dash" else ""
        out.append(f'<text class="il-t" x="10" y="{y + 4}">{name}</text>')
        out.append(f'<rect class="il-mini" x="230" y="{y - 11}" width="34" height="22" rx="4"/><text class="il-s" x="247" y="{y + 4}" text-anchor="middle">B</text>')
        out.append(f'<rect class="il-mini" x="400" y="{y - 11}" width="34" height="22" rx="4"/><text class="il-s" x="417" y="{y + 4}" text-anchor="middle">A</text>')
        if head in ("dia", "diaf"):
            cls = "il-diaf" if head == "diaf" else "il-dia"
            out.append(f'<polygon class="{cls}" points="400,{y} 389,{y - 6} 378,{y} 389,{y + 6}"/>')
            out.append(f'<line class="il-line"{dash} x1="264" y1="{y}" x2="378" y2="{y}"/>')
        else:
            out.append(f'<line class="il-line"{dash} x1="264" y1="{y}" x2="398" y2="{y}"/>')
            if head == "tri":
                out.append(f'<polygon class="il-tri" points="400,{y} 386,{y - 7} 386,{y + 7}"/>')
            else:
                out.append(f'<polyline class="il-open" points="388,{y - 6} 400,{y} 388,{y + 6}"/>')
        out.append(f'<text class="il-s il-mute" x="450" y="{y + 4}">{desc}</text>')
    out.append('<text class="il-s il-mute" x="10" y="268">Ký hiệu trong ô:  + public   − private   # protected   chữ nghiêng = trừu tượng   gạch chân = static</text>')
    return _svg(690, 280, "".join(out), "Bảng ký hiệu UML")


def groups_map(groups):
    """groups: list of (key, title, subtitle, [(id, name)])"""
    out = []
    colw = 300
    for gi, (key, title, sub, items) in enumerate(groups):
        x = 10 + gi * (colw + 15)
        h = 70 + len(items) * 30
        out.append(f'<rect class="il-g il-{key}" x="{x}" y="10" width="{colw}" height="{h}" rx="14"/>')
        out.append(f'<text class="il-gt" x="{x + 16}" y="38">{title}</text>')
        out.append(f'<text class="il-s il-mute" x="{x + 16}" y="58">{sub}</text>')
        for i, (pid, name) in enumerate(items):
            y = 74 + i * 30
            out.append(f'<a href="#{pid}"><rect class="il-chip" x="{x + 14}" y="{y}" width="{colw - 28}" height="24" rx="12"/>'
                       f'<text class="il-s" x="{x + 28}" y="{y + 16}">{name}</text></a>')
    H = 70 + max(len(g[3]) for g in groups) * 30 + 20
    return _svg(10 + 3 * (colw + 15), H, "".join(out), "Ba nhóm mẫu thiết kế")


def composite():
    nodes = [  # (x, y, label, kind)
        (260, 20, "📁 du-an-robot  2583 KB", "c"),
        (80, 110, "📁 src  20 KB", "c"), (260, 110, "📁 docs  2560 KB", "c"), (440, 110, "📄 README.md  3", "l"),
        (0, 200, "📄 main.cpp 12", "l"), (120, 200, "📄 motor.cpp 8", "l"),
        (250, 200, "📄 bao-cao.pdf 2048", "l"), (405, 200, "📁 images  512", "c"),
        (385, 285, "📄 so-do-mach.png 512", "l"),
    ]
    edges = [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (2, 6), (2, 7), (7, 8)]
    W = {0: 200, 1: 130, 2: 150, 3: 140, 4: 110, 5: 115, 6: 140, 7: 120, 8: 165}
    out = []
    for a, b in edges:
        xa, ya = nodes[a][0] + W[a] / 2, nodes[a][1] + 30
        xb, yb = nodes[b][0] + W[b] / 2, nodes[b][1]
        out.append(f'<path class="il-line" d="M{xa},{ya} C{xa},{ya + 30} {xb},{yb - 30} {xb},{yb}" fill="none"/>')
    for i, (x, y, t, k) in enumerate(nodes):
        cls = "il-node-c" if k == "c" else "il-node-l"
        out.append(f'<rect class="{cls}" x="{x}" y="{y}" width="{W[i]}" height="30" rx="8"/>'
                   f'<text class="il-s" x="{x + W[i] / 2}" y="{y + 20}" text-anchor="middle">{t}</text>')
    out.append('<text class="il-s il-mute" x="650" y="40">Composite (nhánh)</text><rect class="il-node-c" x="620" y="28" width="20" height="16" rx="4"/>')
    out.append('<text class="il-s il-mute" x="650" y="68">Leaf (lá)</text><rect class="il-node-l" x="620" y="56" width="20" height="16" rx="4"/>')
    out.append('<text class="il-s il-mute" x="620" y="110">getSize() gọi đệ quy</text><text class="il-s il-mute" x="620" y="128">từ gốc xuống mọi lá,</text><text class="il-s il-mute" x="620" y="146">rồi cộng dồn ngược lên.</text>')
    return _svg(790, 330, "".join(out), "Cây thư mục minh hoạ Composite")


def decorator():
    layers = [("Pearl  +5 000", 300, "il-ring3"), ("CheeseFoam  +10 000", 230, "il-ring2"), ("MilkTea  25 000", 150, "il-ring1")]
    out = []
    cx, cy = 230, 170
    for i, (t, r, cls) in enumerate(layers):
        out.append(f'<ellipse class="{cls}" cx="{cx}" cy="{cy}" rx="{r * 0.72}" ry="{r * 0.5}"/>')
    out.append(f'<text class="il-t" x="{cx}" y="{cy + 5}" text-anchor="middle">🧋 MilkTea</text>')
    out.append(f'<text class="il-s" x="{cx}" y="{cy - 50}" text-anchor="middle">CheeseFoam</text>')
    out.append(f'<text class="il-s" x="{cx}" y="{cy - 105}" text-anchor="middle">Pearl</text>')
    out.append(_arrow_defs("decoA"))
    steps = ["cost() gọi vào  ⟶", "Pearl.cost()", "  → CheeseFoam.cost()", "      → MilkTea.cost() = 25 000", "      ← 25 000 + 10 000", "  ← 35 000 + 5 000", "= 40 000 đ"]
    for i, s in enumerate(steps):
        out.append(f'<text class="il-mono" x="470" y="{70 + i * 26}">{s}</text>')
    return _svg(760, 330, "".join(out), "Các lớp bọc của Decorator")


def chain():
    out = [_arrow_defs("chA")]
    boxes = [("📝 Đơn nghỉ", 10, "il-node-l"), ("Tổ trưởng\n≤ 2 ngày", 170, "il-node-c"),
             ("Hiệu phó\n≤ 5 ngày", 340, "il-node-c"), ("Hiệu trưởng\n≤ 30 ngày", 510, "il-node-c")]
    for t, x, cls in boxes:
        out.append(f'<rect class="{cls}" x="{x}" y="40" width="130" height="58" rx="10"/>')
        for j, line in enumerate(t.split("\n")):
            out.append(f'<text class="il-s" x="{x + 65}" y="{64 + j * 18}" text-anchor="middle">{line}</text>')
    for x in (140, 300, 470):
        out.append(f'<line class="il-line" x1="{x}" y1="69" x2="{x + 28}" y2="69" marker-end="url(#chA)"/>')
    out.append('<text class="il-s il-mute" x="305" y="25" text-anchor="middle">không đủ thẩm quyền → chuyển tiếp “next”</text>')
    for x, t in ((235, "✅ 1 ngày"), (405, "✅ 4 ngày"), (575, "✅ 10 ngày")):
        out.append(f'<line class="il-line" stroke-dasharray="4 3" x1="{x}" y1="98" x2="{x}" y2="128" marker-end="url(#chA)"/>'
                   f'<text class="il-s" x="{x}" y="146" text-anchor="middle">{t}</text>')
    out.append('<line class="il-line" x1="640" y1="69" x2="668" y2="69" marker-end="url(#chA)"/><text class="il-s" x="676" y="74">❌ 45 ngày</text>')
    return _svg(760, 165, "".join(out), "Luồng xử lý của chuỗi trách nhiệm")


def interpreter():
    nodes = {"mul": (230, 20, "*"), "add": (120, 90, "+"), "sub": (340, 90, "−"),
             "x": (70, 160, "x"), "2": (170, 160, "2"), "y": (290, 160, "y"), "1": (390, 160, "1")}
    edges = [("mul", "add"), ("mul", "sub"), ("add", "x"), ("add", "2"), ("sub", "y"), ("sub", "1")]
    out = []
    for a, b in edges:
        out.append(f'<line class="il-line" x1="{nodes[a][0]}" y1="{nodes[a][1] + 18}" x2="{nodes[b][0]}" y2="{nodes[b][1] - 18}"/>')
    for k, (x, y, t) in nodes.items():
        cls = "il-node-c" if t in "*+−" else "il-node-l"
        out.append(f'<circle class="{cls}" cx="{x}" cy="{y}" r="18"/><text class="il-t" x="{x}" y="{y + 5}" text-anchor="middle">{t}</text>')
    out.append('<text class="il-mono" x="470" y="40">Nguồn:  x 2 + y 1 - *</text>')
    out.append('<text class="il-mono" x="470" y="70">Cây  :  (x + 2) * (y − 1)</text>')
    out.append('<text class="il-mono" x="470" y="100">x=5, y=3 → 7 * 2 = 14</text>')
    out.append('<text class="il-s il-mute" x="470" y="140">● tròn đậm: Nonterminal</text>')
    out.append('<text class="il-s il-mute" x="470" y="160">○ tròn nhạt: Terminal (số, biến)</text>')
    return _svg(720, 190, "".join(out), "Cây cú pháp của biểu thức")


def mediator():
    import math
    out = []
    names = ["An", "Bình", "Chi", "Dũng", "Thầy"]
    def ring(cx, cy, r):
        return [(cx + r * math.cos(-math.pi / 2 + i * 2 * math.pi / 5), cy + r * math.sin(-math.pi / 2 + i * 2 * math.pi / 5)) for i in range(5)]
    p1 = ring(150, 140, 95)
    for i in range(5):
        for j in range(i + 1, 5):
            out.append(f'<line class="il-line il-thin" x1="{p1[i][0]:.0f}" y1="{p1[i][1]:.0f}" x2="{p1[j][0]:.0f}" y2="{p1[j][1]:.0f}"/>')
    p2 = ring(480, 140, 105)
    for (x, y) in p2:
        out.append(f'<line class="il-line" x1="{x:.0f}" y1="{y:.0f}" x2="480" y2="140"/>')
    out.append('<rect class="il-node-c" x="430" y="120" width="100" height="40" rx="10"/><text class="il-s" x="480" y="145" text-anchor="middle">ChatRoom</text>')
    for pts in (p1, p2):
        for (x, y), n in zip(pts, names):
            out.append(f'<circle class="il-node-l" cx="{x:.0f}" cy="{y:.0f}" r="22"/><text class="il-s" x="{x:.0f}" y="{y + 5:.0f}" text-anchor="middle">{n}</text>')
    out.append('<text class="il-t" x="150" y="268" text-anchor="middle">Không có Mediator: 10 liên kết</text>')
    out.append('<text class="il-t" x="480" y="268" text-anchor="middle">Có Mediator: 5 liên kết</text>')
    return _svg(640, 285, "".join(out), "So sánh có và không có Mediator")


def observer():
    out = [_arrow_defs("obA")]
    out.append('<rect class="il-node-c" x="20" y="95" width="170" height="60" rx="12"/>'
               '<text class="il-t" x="105" y="121" text-anchor="middle">📡 WeatherStation</text>'
               '<text class="il-s il-mute" x="105" y="141" text-anchor="middle">setMeasurements()</text>')
    obs = [("🖥️ LcdDisplay", 30), ("🌀 AutoFan", 100), ("📱 PhoneApp", 170)]
    for t, y in obs:
        out.append(f'<path class="il-line" d="M190,125 C260,125 260,{y + 20} 320,{y + 20}" fill="none" marker-end="url(#obA)"/>')
        out.append(f'<rect class="il-node-l" x="322" y="{y}" width="150" height="40" rx="10"/><text class="il-s" x="397" y="{y + 25}" text-anchor="middle">{t}</text>')
    out.append('<text class="il-s il-mute" x="250" y="20">update(t, h)</text>')
    out.append('<text class="il-s il-mute" x="490" y="60">subscribe() để nhận</text>')
    out.append('<text class="il-s il-mute" x="490" y="80">unsubscribe() để huỷ</text>')
    out.append('<text class="il-s il-mute" x="490" y="120">Subject chỉ biết interface</text>')
    out.append('<text class="il-s il-mute" x="490" y="140">Observer, không biết LCD,</text>')
    out.append('<text class="il-s il-mute" x="490" y="160">quạt hay điện thoại.</text>')
    return _svg(680, 225, "".join(out), "Subject phát thông báo tới các Observer")


def state():
    out = [_arrow_defs("stA")]
    st = {"no": (110, 120, "Chờ tiền"), "has": (420, 120, "Đã có tiền"), "sold": (420, 300, "Hết hàng")}
    for k, (x, y, t) in st.items():
        out.append(f'<rect class="il-node-c" x="{x - 70}" y="{y - 26}" width="140" height="52" rx="26"/><text class="il-t" x="{x}" y="{y + 5}" text-anchor="middle">{t}</text>')
    out.append('<circle class="il-dot" cx="110" cy="30" r="8"/><line class="il-line" x1="110" y1="38" x2="110" y2="92" marker-end="url(#stA)"/>')
    arrows = [
        ('M180,108 L350,108', "insertCoin()", 265, 100),
        ('M350,134 L180,134', "ejectCoin()", 265, 152),
        ('M420,146 L420,272', "pressButton() [hết hàng]", 430, 215),
        ('M370,140 C300,200 200,200 140,146', "pressButton() [còn hàng]", 175, 210),
        ('M350,300 C200,320 120,260 110,146', "refill()", 150, 300),
    ]
    for d, lbl, lx, ly in arrows:
        out.append(f'<path class="il-line" d="{d}" fill="none" marker-end="url(#stA)"/>'
                   f'<text class="il-s" x="{lx}" y="{ly}">{lbl}</text>')
    out.append('<text class="il-s il-mute" x="520" y="290">insertCoin() khi hết hàng</text><text class="il-s il-mute" x="520" y="308">→ trả lại tiền, giữ nguyên</text>')
    return _svg(720, 340, "".join(out), "Sơ đồ chuyển trạng thái máy bán nước")


EXTRA = {"composite": composite, "decorator": decorator, "chain": chain, "interpreter": interpreter,
         "mediator": mediator, "observer": observer, "state": state}
EXTRA_CAPTION = {
    "composite": "Hình minh hoạ: cây thư mục trong ví dụ — mọi nút đều trả lời được getSize().",
    "decorator": "Hình minh hoạ: các lớp “vỏ” bọc quanh đồ uống gốc, lời gọi đi vào trong rồi cộng dồn ra ngoài.",
    "chain": "Hình minh hoạ: đơn xin nghỉ trôi dọc chuỗi cho tới khi gặp người đủ thẩm quyền.",
    "interpreter": "Hình minh hoạ: cây cú pháp (AST) được dựng từ chuỗi hậu tố.",
    "mediator": "Hình minh hoạ: từ mạng lưới chằng chịt sang mô hình hình sao.",
    "observer": "Hình minh hoạ: một lần thay đổi, mọi observer đã đăng ký đều được báo.",
    "state": "Hình minh hoạ: sơ đồ chuyển trạng thái (state diagram) của máy bán nước.",
}
