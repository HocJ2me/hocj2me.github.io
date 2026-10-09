# -*- coding: utf-8 -*-
"""Vẽ sơ đồ lớp UML đơn giản thành SVG từ đặc tả dạng dict (xem content_*.py)."""
from html import escape
import math

CW = 7.0          # độ rộng 1 ký tự font mono 12px (ước lượng)
LH = 16           # chiều cao dòng thành viên
NOTE_CW, NOTE_LH = 6.7, 15


class Box:
    def __init__(self, bid, name, st, fields, methods, cx, y):
        self.id, self.name, self.st, self.fields, self.methods = bid, name, st, fields, methods
        lines = [name] + fields + methods + ([f"«{st}»"] if st else [])
        self.w = max(110, max(len(s) for s in lines) * CW + 22)
        self.head = 30 + (14 if st else 0)
        h = self.head
        if fields:
            h += 8 + LH * len(fields)
        if methods:
            h += 8 + LH * len(methods)
        if not fields and not methods and st not in (None, "Client") and name != "Client":
            h += 10
        self.h = h
        self.x0, self.y0 = cx - self.w / 2, y
        self.x1, self.y1 = self.x0 + self.w, y + h
        self.cx, self.cy = cx, y + h / 2

    def svg(self):
        kind = {"interface": "u-int", "abstract": "u-abs"}.get(self.st, "u-cls")
        if self.name == "Client" or self.st == "Client":
            kind = "u-cli"
        out = [f'<g class="u-box {kind}">',
               f'<rect x="{self.x0:.1f}" y="{self.y0:.1f}" width="{self.w:.1f}" height="{self.h:.1f}" rx="6"/>',
               f'<rect class="u-head" x="{self.x0:.1f}" y="{self.y0:.1f}" width="{self.w:.1f}" height="{self.head:.1f}" rx="6"/>',
               f'<rect class="u-head" x="{self.x0:.1f}" y="{self.y0 + self.head - 8:.1f}" width="{self.w:.1f}" height="8"/>']
        y = self.y0 + 18
        if self.st:
            out.append(f'<text class="u-st" x="{self.cx:.1f}" y="{y - 2:.1f}" text-anchor="middle">«{escape(self.st)}»</text>')
            y += 14
        italic = ' font-style="italic"' if self.st == "abstract" else ""
        out.append(f'<text class="u-name" x="{self.cx:.1f}" y="{y + 2:.1f}" text-anchor="middle"{italic}>{escape(self.name)}</text>')
        y = self.y0 + self.head
        for group in (self.fields, self.methods):
            if not group:
                continue
            out.append(f'<line class="u-sep" x1="{self.x0:.1f}" y1="{y:.1f}" x2="{self.x1:.1f}" y2="{y:.1f}"/>')
            y += 4
            for line in group:
                y += LH
                cls = "u-mem"
                if "{abstract}" in line:
                    cls += " u-it"
                if "{static}" in line:
                    cls += " u-ul"
                out.append(f'<text class="{cls}" x="{self.x0 + 10:.1f}" y="{y - 3:.1f}">{escape(line)}</text>')
            y += 4
        out.append("</g>")
        return "\n".join(out)


class Note:
    def __init__(self, nid, text, cx, y):
        self.id, self.lines = nid, text.split("\n")
        self.w = max(len(s) for s in self.lines) * NOTE_CW + 24
        self.h = len(self.lines) * NOTE_LH + 14
        self.x0, self.y0 = cx - self.w / 2, y
        self.x1, self.y1 = self.x0 + self.w, y + self.h
        self.cx, self.cy = cx, y + self.h / 2

    def svg(self):
        f = 10
        pts = f"{self.x0:.1f},{self.y0:.1f} {self.x1 - f:.1f},{self.y0:.1f} {self.x1:.1f},{self.y0 + f:.1f} {self.x1:.1f},{self.y1:.1f} {self.x0:.1f},{self.y1:.1f}"
        out = [f'<g class="u-note"><polygon points="{pts}"/>',
               f'<polyline class="u-fold" points="{self.x1 - f:.1f},{self.y0:.1f} {self.x1 - f:.1f},{self.y0 + f:.1f} {self.x1:.1f},{self.y0 + f:.1f}"/>']
        for i, line in enumerate(self.lines):
            out.append(f'<text x="{self.x0 + 10:.1f}" y="{self.y0 + 19 + i * NOTE_LH:.1f}" xml:space="preserve">{escape(line)}</text>')
        out.append("</g>")
        return "\n".join(out)


def _clip(r, px, py):
    """Giao điểm của đoạn từ tâm r tới (px,py) với biên hình chữ nhật r."""
    dx, dy = px - r.cx, py - r.cy
    if dx == 0 and dy == 0:
        return r.cx, r.cy
    hw, hh = (r.x1 - r.x0) / 2, (r.y1 - r.y0) / 2
    t = min(hw / abs(dx) if dx else math.inf, hh / abs(dy) if dy else math.inf)
    return r.cx + dx * t, r.cy + dy * t


def _attach(r, p):
    """Điểm gắn trên biên r hướng tới điểm p (ưu tiên đường thẳng đứng/ngang)."""
    px, py = p
    if r.y0 <= py <= r.y1 and (px > r.x1 or px < r.x0):
        return (r.x1 if px > r.x1 else r.x0), py
    if r.x0 <= px <= r.x1 and (py > r.y1 or py < r.y0):
        return px, (r.y1 if py > r.y1 else r.y0)
    return _clip(r, px, py)


def _head(kind, p, q):
    """Vẽ đầu mũi tên tại p, hướng từ q tới p."""
    ang = math.atan2(p[1] - q[1], p[0] - q[0])
    def pt(d, a):
        return p[0] - d * math.cos(ang + a), p[1] - d * math.sin(ang + a)
    if kind in ("ext", "impl"):
        a, b = pt(14, 0.45), pt(14, -0.45)
        return f'<polygon class="u-tri" points="{p[0]:.1f},{p[1]:.1f} {a[0]:.1f},{a[1]:.1f} {b[0]:.1f},{b[1]:.1f}"/>'
    if kind in ("assoc", "dep"):
        a, b = pt(11, 0.42), pt(11, -0.42)
        return f'<polyline class="u-open" points="{a[0]:.1f},{a[1]:.1f} {p[0]:.1f},{p[1]:.1f} {b[0]:.1f},{b[1]:.1f}"/>'
    return ""


def _diamond(kind, p, q):
    """Hình thoi tại p (phía 'toàn thể'), hướng về q."""
    ang = math.atan2(q[1] - p[1], q[0] - p[0])
    def at(d, side):
        return (p[0] + d * math.cos(ang) + side * 6 * math.cos(ang + math.pi / 2),
                p[1] + d * math.sin(ang) + side * 6 * math.sin(ang + math.pi / 2))
    tip = (p[0] + 22 * math.cos(ang), p[1] + 22 * math.sin(ang))
    a, b = at(11, 1), at(11, -1)
    cls = "u-dia-fill" if kind == "comp" else "u-dia"
    return (f'<polygon class="{cls}" points="{p[0]:.1f},{p[1]:.1f} {a[0]:.1f},{a[1]:.1f} {tip[0]:.1f},{tip[1]:.1f} {b[0]:.1f},{b[1]:.1f}"/>', tip)


def render(spec, title=""):
    items = {}
    for b in spec.get("boxes", []):
        items[b[0]] = Box(*b)
    for n in spec.get("notes", []):
        items[n[0]] = Note(*n)

    edges_svg, labels_svg = [], []
    for e in spec.get("edges", []):
        a, b, kind, label = items[e[0]], items[e[1]], e[2], e[3]
        route = e[4] if len(e) > 4 else None
        if a is b:                                   # tự liên kết (vòng)
            pts = [(a.x1, a.y0 + 22), (a.x1 + 32, a.y0 + 22), (a.x1 + 32, a.y0 - 20), (a.x1 - 34, a.y0 - 20), (a.x1 - 34, a.y0)]
        elif route == "tree":
            start = (a.cx, a.y0) if a.y0 > b.y1 else (a.cx, a.y1)
            end = (b.cx, b.y1) if a.y0 > b.y1 else (b.cx, b.y0)
            midy = (b.y1 + a.y0) / 2 if a.y0 > b.y1 else (a.y1 + b.y0) / 2
            pts = [start, (a.cx, midy), (b.cx, midy), end]
        elif isinstance(route, list):
            pts = [_attach(a, route[0])] + list(route) + [_attach(b, route[-1])]
        else:
            pts = [_clip(a, b.cx, b.cy), _clip(b, a.cx, a.cy)]

        extra = ""
        if kind in ("agg", "comp"):
            extra, tip = _diamond(kind, pts[0], pts[1])
            pts = [tip] + pts[1:]
        dashed = kind in ("impl", "dep", "note")
        cls = "u-edge" + (" u-dash" if dashed else "")
        path = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        edges_svg.append(f'<polyline class="{cls}" points="{path}"/>')
        edges_svg.append(_head(kind, pts[-1], pts[-2]))
        if extra:
            edges_svg.append(extra)
        if label:
            # đặt nhãn ở giữa đoạn dài nhất
            segs = list(zip(pts, pts[1:]))
            (x1, y1), (x2, y2) = max(segs, key=lambda s: math.dist(*s))
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            if a is b:
                mx, my = a.x1 + 34, a.y0 - 4
            w = len(label) * 6.4 + 10
            labels_svg.append(f'<g class="u-lbl"><rect x="{mx - w / 2:.1f}" y="{my - 9:.1f}" width="{w:.1f}" height="16" rx="4"/>'
                              f'<text x="{mx:.1f}" y="{my + 3:.1f}" text-anchor="middle">{escape(label)}</text></g>')

    group_svg = []
    xs, ys = [], []
    for (x, y, w, h, lbl) in spec.get("groups", []):
        group_svg.append(f'<g class="u-grp"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>'
                         f'<text x="{x + 12}" y="{y + h - 8}">{escape(lbl)}</text></g>')
        xs += [x, x + w]; ys += [y, y + h]
    text_svg = []
    for (cx, y, t) in spec.get("texts", []):
        text_svg.append(f'<text class="u-zone" x="{cx}" y="{y}" text-anchor="middle">{escape(t)}</text>')
        xs += [cx - len(t) * 4, cx + len(t) * 4]; ys += [y - 12, y]

    for it in items.values():
        xs += [it.x0, it.x1]; ys += [it.y0, it.y1]
    for e in spec.get("edges", []):
        if e[0] == e[1]:
            it = items[e[0]]
            xs.append(it.x1 + 70); ys.append(it.y0 - 30)
        if len(e) > 4 and isinstance(e[4], list):
            for (x, y) in e[4]:
                xs.append(x + 30); ys.append(y)
    m = 16
    minx, miny, maxx, maxy = min(xs) - m, min(ys) - m, max(xs) + m, max(ys) + m
    W, H = maxx - minx, maxy - miny
    body = "\n".join(group_svg + text_svg + edges_svg + labels_svg + [i.svg() for i in items.values()])
    return (f'<svg class="uml" viewBox="{minx:.0f} {miny:.0f} {W:.0f} {H:.0f}" style="max-width:{W:.0f}px" '
            f'role="img" aria-label="Sơ đồ lớp UML {escape(title)}" xmlns="http://www.w3.org/2000/svg">\n{body}\n</svg>')
