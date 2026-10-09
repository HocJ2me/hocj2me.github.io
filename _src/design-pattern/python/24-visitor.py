"""Visitor – Python 3. Python không có nạp chồng hàm theo kiểu, nên dùng tên visit_<lớp>
và tra bằng getattr. Cuối file: cách hiện đại với match/case (Python 3.10+)."""
import json
import math
from dataclasses import dataclass, asdict


class Shape:
    def accept(self, visitor):
        # double dispatch: chọn phương thức theo tên lớp của chính phần tử
        return getattr(visitor, "visit_" + type(self).__name__.lower())(self)


@dataclass
class Circle(Shape):
    r: float


@dataclass
class Rectangle(Shape):
    w: float
    h: float


@dataclass
class Triangle(Shape):
    base: float
    height: float


class AreaVisitor:
    def __init__(self): self.total = 0.0

    def _add(self, label, a):
        print(f"  {a:6.2f}  <- {label}")
        self.total += a

    def visit_circle(self, c): self._add("Hình tròn", math.pi * c.r ** 2)
    def visit_rectangle(self, r): self._add("Chữ nhật", r.w * r.h)
    def visit_triangle(self, t): self._add("Tam giác", t.base * t.height / 2)


class JsonExportVisitor:
    def __init__(self): self.items = []
    def visit_circle(self, c): self.items.append({"type": "circle", **asdict(c)})
    def visit_rectangle(self, r): self.items.append({"type": "rect", **asdict(r)})
    def visit_triangle(self, t): self.items.append({"type": "triangle", **asdict(t)})


def area(shape) -> float:                           # Python 3.10+: structural pattern matching
    match shape:
        case Circle(r=r): return math.pi * r * r
        case Rectangle(w=w, h=h): return w * h
        case Triangle(base=b, height=h): return b * h / 2


if __name__ == "__main__":
    drawing = [Circle(2), Rectangle(3, 4), Triangle(6, 5)]
    av = AreaVisitor()
    for s in drawing:
        s.accept(av)
    print(f"Tổng diện tích: {av.total:.2f}")
    print("-- Xuất JSON --")
    jv = JsonExportVisitor()
    for s in drawing:
        s.accept(jv)
    print(json.dumps(jv.items, indent=2))
    print("-- match/case --")
    print(f"Tổng diện tích: {sum(area(s) for s in drawing):.2f}")
