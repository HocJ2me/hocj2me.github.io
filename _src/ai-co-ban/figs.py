# -*- coding: utf-8 -*-
"""Hình minh hoạ cho khóa AI cơ bản — biểu đồ vẽ từ DỮ LIỆU THẬT (numpy / scikit-learn) lúc build."""
import numpy as np
from svg import svg, box, text, arrow, path

DOT = ["fa", "fe", "fd", "fc"]


def dot(x, y, cls, r=4):
    return f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="{r}"/>'


def line(x1, y1, x2, y2, cls="ln"):
    return f'<line class="{cls}" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>'


def poly(pts, cls="ln"):
    return f'<polyline class="{cls}" fill="none" points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}"/>'


class Axes:
    """Khung toạ độ: đổi số liệu thật -> toạ độ điểm ảnh."""

    def __init__(self, x0, y0, w, h, xr, yr):
        self.x0, self.y0, self.w, self.h, self.xr, self.yr = x0, y0, w, h, xr, yr

    def X(self, v):
        return self.x0 + (v - self.xr[0]) / (self.xr[1] - self.xr[0]) * self.w

    def Y(self, v):
        return self.y0 + self.h - (v - self.yr[0]) / (self.yr[1] - self.yr[0]) * self.h

    def frame(self, xlabel, ylabel, xt=(), yt=()):
        b = [line(self.x0, self.y0 + self.h, self.x0 + self.w, self.y0 + self.h), line(self.x0, self.y0, self.x0, self.y0 + self.h)]
        for v in xt:
            b.append(line(self.X(v), self.y0 + self.h, self.X(v), self.y0 + self.h + 4))
            b.append(text(self.X(v), self.y0 + self.h + 16, f"{v:g}", "xs mute", "middle"))
        for v in yt:
            b.append(line(self.x0 - 4, self.Y(v), self.x0, self.Y(v)))
            b.append(text(self.x0 - 7, self.Y(v) + 4, f"{v:g}", "xs mute", "end"))
        b.append(text(self.x0 + self.w, self.y0 + self.h + 32, xlabel, "xs", "end"))
        b.append(text(self.x0 - 30, self.y0 - 10, ylabel, "xs"))
        return "".join(b)


# ---------------------------------------------------------------- bài 1
def ai_venn():
    b = ['<ellipse class="bx-g" cx="300" cy="130" rx="290" ry="122"/>', '<ellipse class="bx-b" cx="340" cy="150" rx="210" ry="92"/>',
         '<ellipse class="bx-a" cx="380" cy="168" rx="125" ry="60"/>']
    b += [text(40, 70, "TRÍ TUỆ NHÂN TẠO (AI)", "t"), text(40, 90, "máy làm việc “thông minh”: luật if-else, tìm đường, chơi cờ…", "xs mute"),
          text(170, 110, "HỌC MÁY (Machine Learning)", "t"), text(170, 128, "máy tự rút ra quy luật từ dữ liệu", "xs mute"),
          text(380, 165, "HỌC SÂU (Deep Learning)", "s", "middle"), text(380, 183, "mạng nơ-ron nhiều lớp", "xs mute", "middle"),
          text(380, 199, "nhận dạng ảnh, giọng nói, ChatGPT", "xs mute", "middle")]
    return svg(600, 262, "".join(b), "AI, học máy và học sâu")


def lap_trinh_vs_hoc_may():
    b = [text(20, 22, "Lập trình truyền thống", "t"), text(380, 22, "Học máy", "t")]
    b += [box(20, 40, 110, 36, "bx-c", text="Dữ liệu"), box(20, 90, 110, 36, "bx-d", text="Luật (người viết)"),
          box(170, 62, 120, 42, "bx-g", text="Chương trình"), arrow(130, 58, 168, 76), arrow(130, 108, 168, 92),
          arrow(230, 104, 230, 140), box(170, 140, 120, 36, "bx-a", text="Kết quả")]
    b += [box(380, 40, 110, 36, "bx-c", text="Dữ liệu"), box(380, 90, 110, 36, "bx-a", text="Kết quả đúng (nhãn)"),
          box(530, 62, 120, 42, "bx-g", text="Huấn luyện"), arrow(490, 58, 528, 76), arrow(490, 108, 528, 92),
          arrow(590, 104, 590, 140), box(530, 140, 120, 36, "bx-d", text="Luật = MÔ HÌNH")]
    return svg(670, 190, "".join(b), "Lập trình truyền thống so với học máy")


def scatter_iris_1d():
    from sklearn.datasets import load_iris
    iris = load_iris()
    X, y = iris.data[50:, 2], iris.target[50:] - 1
    ax = Axes(40, 30, 560, 80, (2.8, 7.1), (0, 1))
    b = [ax.frame("chiều dài cánh hoa (cm)", "", xt=[3, 4, 5, 6, 7])]
    rng = np.random.default_rng(0)
    for v, k in zip(X, y):
        b.append(dot(ax.X(v), 50 + 30 * k + rng.uniform(-8, 8), DOT[k], 4))
    b.append(text(46, 46, "versicolor", "xs"))
    b.append(text(46, 76 + 30, "virginica", "xs"))
    for v, c, lab in ((5.5, "dash", "luật tự viết 5.5 → đúng 75%"), (4.75, "ln", "máy học: 4.7 → đúng 93%")):
        b.append(line(ax.X(v), 22, ax.X(v), 112, c))
        b.append(text(ax.X(v) + (6 if v > 5 else -6), 18, lab, "xs", "start" if v > 5 else "end"))
    return svg(640, 160, "".join(b), "Dữ liệu chiều dài cánh hoa của hai loài")


# ---------------------------------------------------------------- bài 2
def bang_du_lieu():
    hdr = ["dien_tich", "so_phong", "cach_tt_km", "gia (tỉ)"]
    rows = [["45", "2", "3.5", "2.6"], ["80", "3", "8.0", "4.1"], ["120", "4", "1.2", "6.9"], ["60", "2", "5.1", "?"]]
    b = [text(10, 18, "Mỗi HÀNG là một mẫu (sample), mỗi CỘT là một đặc trưng (feature); cột cuối là NHÃN (label) cần dự đoán", "xs mute")]
    for j, h in enumerate(hdr):
        b.append(box(20 + j * 120, 30, 116, 30, "bx-a" if j == 3 else "bx-c", rx=4, text=h, tcls="xs"))
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            b.append(box(20 + j * 120, 64 + i * 30, 116, 28, "bx-d" if v == "?" else "bx", rx=4, text=v, tcls="mono"))
    b.append(text(510, 80, "X = 3 cột đầu", "s"))
    b.append(text(510, 100, "  shape (số mẫu, 3)", "xs mute"))
    b.append(text(510, 130, "y = cột giá", "s"))
    b.append(text(510, 165, "← mẫu mới: mô hình", "xs"))
    b.append(text(510, 181, "   phải đoán “?”", "xs"))
    return svg(650, 190, "".join(b), "Bảng dữ liệu: mẫu, đặc trưng, nhãn")


def chuan_hoa():
    ax1 = Axes(40, 30, 250, 120, (0, 130), (0, 9))
    rng = np.random.default_rng(2)
    s = rng.uniform(30, 120, 25)
    p = rng.uniform(1, 5, 25).round()
    b = [ax1.frame("diện tích m²", "số phòng", xt=[0, 50, 100], yt=[0, 4, 8]), text(40, 14, "Chưa chuẩn hoá: thang đo lệch nhau", "xs")]
    b += [dot(ax1.X(a), ax1.Y(c), "bx-a", 3.5) for a, c in zip(s, p)]
    ax2 = Axes(380, 30, 230, 120, (-2.2, 2.2), (-2.2, 2.2))
    b += [ax2.frame("z diện tích", "z phòng", xt=[-2, 0, 2], yt=[-2, 0, 2]), text(380, 14, "z-score: cùng thang, trung bình 0", "xs")]
    zs, zp = (s - s.mean()) / s.std(), (p - p.mean()) / p.std()
    b += [dot(ax2.X(a), ax2.Y(c), "bx-b", 3.5) for a, c in zip(zs, zp)]
    b.append(arrow(300, 90, 350, 90, label="(x − μ) / σ"))
    return svg(640, 190, "".join(b), "Chuẩn hoá dữ liệu")


# ---------------------------------------------------------------- bài 3
def _nha():
    rng = np.random.default_rng(0)
    s = rng.uniform(30, 120, 40)
    g = 0.045 * s + 0.5 + rng.normal(0, 0.35, 40)
    a, c = np.polyfit(s, g, 1)
    return s, g, a, c


def hoi_quy_plot():
    s, g, a, c = _nha()
    ax = Axes(50, 20, 520, 200, (25, 125), (0, 7))
    b = [ax.frame("diện tích (m²)", "giá (tỉ đồng)", xt=[30, 60, 90, 120], yt=[0, 2, 4, 6])]
    for xi, yi in zip(s[:12], g[:12]):
        b.append(line(ax.X(xi), ax.Y(yi), ax.X(xi), ax.Y(a * xi + c), "dash"))
    b += [dot(ax.X(xi), ax.Y(yi), "fa", 4) for xi, yi in zip(s, g)]
    b.append(line(ax.X(25), ax.Y(a * 25 + c), ax.X(125), ax.Y(a * 125 + c)))
    b.append(text(ax.X(28), 34, f"đường thẳng tốt nhất: giá = {a:.4f}·x + {c:.2f}", "s"))
    b.append(text(ax.X(28), 52, "nét đứt = sai số từng điểm", "xs mute"))
    return svg(600, 262, "".join(b), "Hồi quy tuyến tính")


def gradient_descent():
    ax = Axes(50, 20, 300, 180, (-0.2, 2.6), (0, 2.2))
    ws = np.linspace(-0.2, 2.6, 80)
    L = lambda w: 0.32 * (w - 1.27) ** 2 + 0.14
    b = [ax.frame("trọng số w", "mất mát", xt=[0, 1, 2], yt=[0, 1, 2]), poly([(ax.X(w), ax.Y(L(w))) for w in ws])]
    w = -0.1
    for i in range(6):
        w2 = w - 0.9 * 2 * 0.32 * (w - 1.27)
        b.append(dot(ax.X(w), ax.Y(L(w)), "bx-d", 5))
        b.append(f'<line class="ln" x1="{ax.X(w):.1f}" y1="{ax.Y(L(w)):.1f}" x2="{ax.X(w2):.1f}" y2="{ax.Y(L(w2)):.1f}" marker-end="url(#MARK)"/>')
        w = w2
    b.append(dot(ax.X(1.27), ax.Y(0.14), "bx-a", 6))
    b.append(text(ax.X(1.27), ax.Y(0.14) + 22, "đáy: w tốt nhất", "xs", "middle"))
    b += [text(390, 50, "Gradient descent = xuống dốc", "t"), text(390, 76, "1. Tính độ dốc (đạo hàm) tại chỗ đang đứng", "xs"),
          text(390, 96, "2. Bước NGƯỢC chiều dốc:", "xs"), text(400, 116, "w ← w − tốc_độ_học × dốc", "mono"),
          text(390, 140, "3. Lặp lại tới khi gần như không đổi", "xs"),
          text(390, 172, "tốc độ học quá nhỏ → đi rất chậm", "xs mute"), text(390, 190, "quá lớn → nhảy qua đáy, phân kỳ", "xs mute")]
    return svg(660, 240, "".join(b), "Gradient descent")


# ---------------------------------------------------------------- bài 4
def knn_plot():
    from sklearn.datasets import load_iris
    iris = load_iris()
    X, y = iris.data[:, 2:4], iris.target
    ax = Axes(50, 20, 420, 220, (0.8, 7.1), (0, 2.6))
    b = [ax.frame("dài cánh hoa (cm)", "rộng (cm)", xt=[1, 3, 5, 7], yt=[0, 1, 2])]
    q = np.array([4.9, 1.7])
    d = np.sqrt(((X - q) ** 2).sum(1))
    near = np.argsort(d)[:5]
    r = d[near[-1]]
    b.append(f'<ellipse class="dash" fill="none" cx="{ax.X(q[0]):.1f}" cy="{ax.Y(q[1]):.1f}" rx="{r / 6.3 * 420:.1f}" ry="{r / 2.6 * 220:.1f}"/>')
    b += [dot(ax.X(a), ax.Y(c), DOT[k], 3.5) for (a, c), k in zip(X, y)]
    for i in near:
        b.append(line(ax.X(q[0]), ax.Y(q[1]), ax.X(X[i, 0]), ax.Y(X[i, 1]), "ln"))
    b.append(f'<rect class="bx-b" style="stroke-width:2.5" x="{ax.X(q[0]) - 7:.1f}" y="{ax.Y(q[1]) - 7:.1f}" width="14" height="14"/>')
    lab = [(iris.target_names[k], DOT[k]) for k in range(3)]
    for i, (n, c) in enumerate(lab):
        b += [dot(500, 40 + i * 22, c, 5), text(512, 44 + i * 22, n, "xs")]
    b += [f'<rect class="bx-b" style="stroke-width:2.5" x="494" y="{40 + 3 * 22 - 6}" width="12" height="12"/>', text(512, 44 + 66, "hoa cần đoán", "xs"),
          text(494, 150, "5 láng giềng gần nhất", "xs"), text(494, 166, "bỏ phiếu → nhãn đa số", "xs"),
          text(494, 192, f"→ {sum(y[near] == 2)} virginica, {sum(y[near] == 1)} versicolor", "xs mute")]
    return svg(660, 275, "".join(b), "Thuật toán kNN")


def chia_du_lieu():
    b = [box(20, 30, 420, 40, "bx-a", text="70% dữ liệu HỌC (train) – mô hình được nhìn", tcls="s"),
         box(440, 30, 180, 40, "bx-d", text="30% KIỂM TRA (test)", tcls="s"),
         text(20, 20, "Không bao giờ chấm điểm mô hình trên dữ liệu nó đã học — giống cho học sinh làm lại đúng đề đã chữa", "xs mute"),
         text(230, 92, "fit(X_hoc, y_hoc)", "mono", "middle"), text(530, 92, "score(X_thu, y_thu)", "mono", "middle")]
    return svg(640, 104, "".join(b), "Chia dữ liệu học và kiểm tra")


# ---------------------------------------------------------------- bài 5
def ma_tran_nham_lan():
    v = [[50, 3], [3, 87]]
    lab = [["Đúng: ác tính", "SAI: bỏ sót ca bệnh!"], ["SAI: báo động nhầm", "Đúng: lành"]]
    cls = [["bx-d", "bx-e"], ["bx-b", "bx-d"]]
    b = [text(250, 20, "DỰ ĐOÁN", "s", "middle"), text(170, 42, "ác tính", "xs", "middle"), text(330, 42, "lành", "xs", "middle"),
         text(30, 120, "THẬT", "s"), text(80, 86, "ác tính", "xs", "end"), text(80, 166, "lành", "xs", "end")]
    for i in range(2):
        for j in range(2):
            b.append(box(90 + j * 160, 50 + i * 80, 156, 76, cls[i][j], rx=6, text=str(v[i][j]), sub=lab[i][j], tcls="t"))
    b += [text(440, 70, "Accuracy = (50 + 87) / 143 = 95.8%", "xs"), text(440, 96, "Recall ác tính = 50 / (50+3)", "xs"),
          text(440, 112, "  = tìm ra bao nhiêu % ca bệnh", "xs mute"), text(440, 138, "Precision = trong số đã báo,", "xs"),
          text(440, 154, "  bao nhiêu % báo đúng", "xs mute"), text(440, 190, "Y tế: ưu tiên RECALL cao", "s")]
    return svg(680, 214, "".join(b), "Ma trận nhầm lẫn")


def qua_khop():
    rng = np.random.default_rng(3)
    x = np.sort(rng.uniform(0, 1, 15))
    yv = np.sin(2 * np.pi * x) + rng.normal(0, 0.2, 15)
    xs = np.linspace(x.min(), x.max(), 120)
    b = []
    for k, (d, ten) in enumerate(((1, "bậc 1: chưa khớp"), (3, "bậc 3: vừa đẹp"), (9, "bậc 9: quá khớp"))):
        ax = Axes(20 + k * 215, 30, 190, 120, (0, 1), (-1.8, 1.8))
        b.append(f'<rect class="bx" x="{ax.x0}" y="{ax.y0}" width="190" height="120" rx="4"/>')
        b.append(text(ax.x0 + 95, 20, ten, "s", "middle"))
        ys = np.clip(np.polyval(np.polyfit(x, yv, d), xs), -1.8, 1.8)
        b.append(poly([(ax.X(a), ax.Y(c)) for a, c in zip(xs, ys)], "ln"))
        b.append(poly([(ax.X(a), ax.Y(np.sin(2 * np.pi * a))) for a in xs], "dash"))
        b += [dot(ax.X(a), ax.Y(c), "bx-a", 3.5) for a, c in zip(x, yv)]
    b.append(text(20, 172, "nét đứt = quy luật thật; nét liền = mô hình. Mô hình quá khớp đi qua mọi điểm nhưng dự đoán điểm mới rất sai.", "xs mute"))
    return svg(670, 182, "".join(b), "Chưa khớp, vừa khớp, quá khớp")


# ---------------------------------------------------------------- bài 6
def cay_fig():
    b = ['<polygon class="bx-b" points="300,10 400,40 300,70 200,40"/>', text(300, 44, "độ ẩm ≤ 34.7% ?", "s", "middle"),
         arrow(240, 58, 160, 100, label="đúng", lx=185, ly=72), arrow(360, 58, 440, 100, label="sai", lx=420, ly=72),
         '<polygon class="bx-b" points="160,100 250,128 160,156 70,128"/>', text(160, 132, "mưa ≤ 62% ?", "s", "middle"),
         '<polygon class="bx-b" points="440,100 540,128 440,156 340,128"/>', text(440, 132, "nhiệt độ ≤ 36.4° ?", "s", "middle"),
         arrow(110, 146, 70, 186), arrow(210, 146, 250, 186), arrow(390, 146, 350, 186), arrow(490, 146, 530, 186),
         box(20, 186, 100, 34, "bx-a", text="TƯỚI"), box(200, 186, 110, 34, "bx-c", text="xét nhiệt độ…"),
         box(290 + 10, 186, 100, 34, "bx-d", text="không tưới"), box(480, 186, 110, 34, "bx-c", text="xét độ ẩm…"),
         text(300, 246, "Mỗi nút hỏi MỘT câu Có/Không về một đặc trưng; lá cho ra nhãn. Máy chọn câu hỏi chia dữ liệu “sạch” nhất (Gini nhỏ nhất).", "xs mute", "middle")]
    return svg(610, 256, "".join(b), "Cây quyết định")


# ---------------------------------------------------------------- bài 7
def kmeans_plot():
    rng = np.random.default_rng(5)
    tam_that = np.array([[2, 3], [8, 8], [9, 2]])
    X = np.vstack([rng.normal(t, 1.0, (30, 2)) for t in tam_that])
    tam0 = X[rng.choice(len(X), 3, replace=False)]
    tam = tam0.copy()
    for _ in range(10):
        nhom = np.linalg.norm(X[:, None] - tam[None], axis=2).argmin(1)
        tam = np.array([X[nhom == j].mean(0) for j in range(3)])
    b = []
    for k, (ten, show_grp, T) in enumerate((("Bước 0: dữ liệu chưa có nhãn, 3 tâm ngẫu nhiên", False, tam0), ("Sau khi hội tụ: 3 cụm, 3 trạm xe", True, tam))):
        ax = Axes(40 + k * 320, 34, 260, 180, (-1, 12), (-1, 11))
        b.append(ax.frame("x (km)", "y", xt=[0, 5, 10], yt=[0, 5, 10]))
        b.append(text(ax.x0, 16, ten, "xs"))
        b += [dot(ax.X(p[0]), ax.Y(p[1]), DOT[nhom[i]] if show_grp else "bx", 3.5) for i, p in enumerate(X)]
        b += [f'<path class="bx-g" d="M{ax.X(t[0]):.1f},{ax.Y(t[1]) - 9:.1f} l8,15 h-16 z"/>' for t in T]
    return svg(660, 250, "".join(b), "Phân cụm k-means")


# ---------------------------------------------------------------- bài 8
def noron():
    b = [box(20, 30, 70, 32, "bx-c", text="x₁"), box(20, 100, 70, 32, "bx-c", text="x₂"), box(20, 170, 70, 32, "bx-c", text="1 (bias)"),
         '<circle class="bx-b" cx="280" cy="116" r="46"/>', text(280, 112, "Σ wᵢxᵢ + b", "s", "middle"), text(280, 130, "rồi hàm kích hoạt", "xs mute", "middle"),
         arrow(90, 46, 236, 100, label="× w₁", lx=160, ly=62), arrow(90, 116, 234, 116, label="× w₂", lx=160, ly=110),
         arrow(90, 186, 236, 134, label="× b", lx=160, ly=170), arrow(326, 116, 410, 116), box(410, 98, 90, 36, "bx-a", text="đầu ra"),
         text(530, 50, "Hàm kích hoạt", "s")]
    ax = Axes(530, 70, 110, 60, (-5, 5), (0, 1))
    b.append(poly([(ax.X(z), ax.Y(1 / (1 + np.exp(-z)))) for z in np.linspace(-5, 5, 40)]))
    b.append(line(ax.x0, ax.y0 + ax.h, ax.x0 + ax.w, ax.y0 + ax.h, "thin"))
    b += [text(585, 150, "sigmoid: 0…1", "xs mute", "middle"), text(530, 190, "Học = chỉnh w, b", "xs"), text(530, 206, "cho đầu ra đúng", "xs")]
    return svg(660, 222, "".join(b), "Một nơ-ron nhân tạo")


def xor_fig():
    b = []
    for k, (ten, out, sep) in enumerate((("AND", [0, 0, 0, 1], True), ("OR", [0, 1, 1, 1], True), ("XOR", [0, 1, 1, 0], False))):
        ax = Axes(30 + k * 215, 30, 150, 120, (-0.3, 1.3), (-0.3, 1.3))
        b.append(f'<rect class="bx" x="{ax.x0}" y="{ax.y0}" width="150" height="120" rx="4"/>')
        b.append(text(ax.x0 + 75, 20, ten + (" – 1 đường thẳng chia được" if sep else " – KHÔNG chia được"), "xs", "middle"))
        if ten == "AND":
            b.append(line(ax.X(1.3), ax.Y(0.2), ax.X(0.2), ax.Y(1.3), "ln"))
        if ten == "OR":
            b.append(line(ax.X(0.8), ax.Y(-0.3), ax.X(-0.3), ax.Y(0.8), "ln"))
        for (a, c), o in zip([(0, 0), (0, 1), (1, 0), (1, 1)], out):
            b.append(dot(ax.X(a), ax.Y(c), "bx-a" if o else "bx-e", 8))
            b.append(text(ax.X(a), ax.Y(c) + 4, str(o), "xs", "middle"))
    return svg(670, 160, "".join(b), "AND, OR và XOR")


def _net(lop, nhan, w, h, ox=0):
    xs = [ox + 80 + i * (w - 160) / (len(lop) - 1) for i in range(len(lop))]
    pos = [[(xs[i], h / 2 + (j - (n - 1) / 2) * min(36, (h - 40) / max(n, 1))) for j in range(n)] for i, n in enumerate(lop)]
    b = []
    for i in range(len(lop) - 1):
        for p in pos[i]:
            for q in pos[i + 1]:
                b.append(line(p[0], p[1], q[0], q[1], "ln thin"))
    for i, col in enumerate(pos):
        b += [dot(x, y, ["bx-c", "bx-b", "bx-a"][min(i, 2) if i < len(lop) - 1 else 2], 11) for x, y in col]
        b.append(text(xs[i], h - 4, nhan[i], "xs", "middle"))
    return "".join(b)


def mang_no_ron(lop=(2, 4, 1), nhan=("đầu vào", "lớp ẩn", "đầu ra"), w=560, h=200):
    return svg(w, h + 6, _net(lop, nhan, w, h), "Mạng nơ-ron nhiều lớp")


def lan_truyen():
    b = [box(20, 40, 120, 40, "bx-c", text="Đầu vào X"), box(180, 40, 120, 40, "bx-b", text="Lớp ẩn h"), box(340, 40, 120, 40, "bx-a", text="Đầu ra ŷ"),
         box(500, 40, 140, 40, "bx-d", text="Mất mát L(ŷ, y)"), arrow(140, 52, 178, 52), arrow(300, 52, 338, 52), arrow(460, 52, 498, 52),
         text(330, 26, "① lan truyền XUÔI: tính dự đoán", "xs", "middle"),
         path("M570,80 Q570,120 400,120 L 250,120 Q 230,120 230,84"), text(400, 140, "② lan truyền NGƯỢC: đạo hàm ∂L/∂w theo quy tắc chuỗi", "xs", "middle"),
         text(330, 166, "③ cập nhật: w ← w − tốc_độ_học × ∂L/∂w   (lặp lại hàng nghìn lần)", "xs", "middle")]
    return svg(660, 176, "".join(b), "Lan truyền xuôi và ngược")


# ---------------------------------------------------------------- bài 9
def chu_so_grid():
    from sklearn.datasets import load_digits
    so = load_digits()
    b = [text(10, 16, "10 ảnh mẫu 8×8 điểm trong bộ dữ liệu digits (đã phóng to) — máy chỉ thấy 64 con số độ sáng", "xs mute")]
    for k in range(10):
        img = so.images[np.where(so.target == k)[0][0]]
        x0 = 10 + k * 64
        for i in range(8):
            for j in range(8):
                v = img[i, j] / 16
                if v > 0.05:
                    b.append(f'<rect x="{x0 + j * 7}" y="{26 + i * 7}" width="7" height="7" class="fa" style="opacity:{v:.2f}"/>')
        b.append(f'<rect class="thin" fill="none" x="{x0}" y="26" width="56" height="56"/>')
        b.append(text(x0 + 28, 98, str(k), "s", "middle"))
    return svg(650, 106, "".join(b), "Ảnh chữ số viết tay")


def anh_thanh_vecto():
    b = [box(10, 70, 80, 80, "bx-c", text="ảnh 8×8"), arrow(90, 110, 130, 110, label="duỗi", lx=110, ly=100),
         box(130, 92, 120, 36, "bx", text="64 con số", tcls="xs"), arrow(250, 110, 300, 110),
         _net((6, 5, 4), ("64 đầu vào", "64 nơ-ron ẩn", "10 đầu ra"), 360, 210, ox=240),
         text(620, 60, "đầu ra lớn nhất", "xs"), text(620, 76, "= chữ số dự đoán", "xs")]
    return svg(720, 220, "".join(b), "Ảnh thành vectơ đưa vào mạng")


# ---------------------------------------------------------------- bài 10
def tinyml_flow():
    st = [("Thu dữ liệu", "MPU6050 → Serial → CSV", "bx-c"), ("Trích đặc trưng", "độ lệch, max, biến thiên", "bx-b"),
          ("Huấn luyện", "Python + scikit-learn", "bx-g"), ("Xuất mô hình", "cây → hàm C / TFLite", "bx-a"), ("Chạy trên ESP32", "suy luận vài µs", "bx-d")]
    b = []
    for i, (t, s, c) in enumerate(st):
        x = 10 + i * 144
        b.append(box(x, 30, 132, 58, c, text=t, sub=s, tcls="s"))
        if i:
            b.append(arrow(x - 12, 59, x, 59))
    b.append(text(10, 18, "Quy trình TinyML: huấn luyện trên MÁY TÍNH, chạy (suy luận) trên VI ĐIỀU KHIỂN", "xs mute"))
    b.append(path("M652,88 Q652,126 360,126 Q 76,126 76,92"))
    b.append(text(360, 144, "chạy thử thực tế, thu thêm dữ liệu khi đoán sai → huấn luyện lại", "xs mute", "middle"))
    return svg(720, 154, "".join(b), "Quy trình TinyML")


def tin_hieu_gia_toc():
    rng = np.random.default_rng(11)
    t = np.arange(50) / 50
    sig = [1 + rng.normal(0, 0.02, 50), 1 + 0.25 * np.sin(2 * np.pi * 2 * t + 1) + rng.normal(0, 0.05, 50),
           1 + 0.8 * np.abs(np.sin(2 * np.pi * 3 * t + 2)) + rng.normal(0, 0.1, 50)]
    nga = 1 + rng.normal(0, 0.05, 50)
    nga[20:23] += 2.5
    nga[23:] = rng.normal(0.95, 0.03, 27)
    sig.append(nga)
    ten = ["đứng yên", "đi bộ", "chạy", "NGÃ"]
    b = []
    for k, s in enumerate(sig):
        ax = Axes(30 + k * 160, 30, 140, 100, (0, 1), (0, 3.8))
        b.append(f'<rect class="bx" x="{ax.x0}" y="{ax.y0}" width="140" height="100" rx="4"/>')
        b.append(text(ax.x0 + 70, 20, ten[k], "s", "middle"))
        b.append(poly([(ax.X(a), ax.Y(c)) for a, c in zip(t, s)]))
    b.append(text(30, 150, "Độ lớn gia tốc |a| (đơn vị g) trong 1 giây, 50 mẫu — mỗi hoạt động có “chữ ký” riêng", "xs mute"))
    return svg(670, 160, "".join(b), "Tín hiệu gia tốc của các hoạt động")
