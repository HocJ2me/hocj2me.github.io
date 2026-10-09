"""Prototype – Python 3. Module copy có sẵn: copy.copy (shallow) và copy.deepcopy (deep)."""
import copy


class ExamPaper:
    def __init__(self, title):
        self.title = title
        self.code = "Đề gốc"
        self.questions = []

    def clone(self):
        return copy.deepcopy(self)          # sao chép sâu: list questions cũng được nhân bản

    def __str__(self):
        return f"{self.code} ({self.title}): {len(self.questions)} câu"


class Circle:
    def __init__(self, radius, color):
        self.radius, self.color, self.x, self.y = radius, color, 0, 0

    def clone(self):
        return copy.copy(self)              # chỉ có field kiểu bất biến -> shallow là đủ

    def move(self, dx, dy):
        self.x += dx; self.y += dy

    def __str__(self):
        return f"Circle(r={self.radius}, {self.color}, @{self.x},{self.y})"


class ShapeRegistry:
    def __init__(self):
        self._prototypes = {"red-circle": Circle(10, "đỏ"), "big-blue-circle": Circle(40, "xanh")}

    def get(self, key):
        return self._prototypes[key].clone()


if __name__ == "__main__":
    template = ExamPaper("Đề kiểm tra Python – 45 phút")
    template.questions += ["Singleton là gì?", "Phân biệt Factory Method và Abstract Factory."]

    de_a = template.clone()
    de_a.code = "Mã đề 101"
    de_a.questions.append("Viết Builder cho lớp Student.")
    print(template)
    print(de_a)
    print("Dùng chung list câu hỏi?", de_a.questions is template.questions)

    # Cạm bẫy shallow copy
    de_b = copy.copy(template)
    de_b.questions.append("Câu hỏi thêm vào bản shallow copy")
    print("Sau khi sửa bản shallow, đề gốc có:", len(template.questions), "câu  <- bị ảnh hưởng!")

    reg = ShapeRegistry()
    c1, c2 = reg.get("red-circle"), reg.get("red-circle")
    c2.move(50, 50)
    print(c1, " | ", c2, " | cùng đối tượng?", c1 is c2)
