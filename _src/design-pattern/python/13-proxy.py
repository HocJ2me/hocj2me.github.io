"""Proxy – Python 3."""
from abc import ABC, abstractmethod


class Image(ABC):
    @abstractmethod
    def display(self): ...


class RealImage(Image):
    def __init__(self, file):
        self.file = file
        print(f"  ⏳ Đang tải {file} từ ổ đĩa (rất chậm)...")

    def display(self): print(f"  🖼️  Hiển thị {self.file}")


class LazyImageProxy(Image):
    def __init__(self, file):
        self.file = file
        self._real = None

    def display(self):
        if self._real is None:
            self._real = RealImage(self.file)
        self._real.display()


class RealScoreService:
    def __init__(self): self._db = {"An": 8.0}

    def get_score(self, s):
        print("  (truy vấn cơ sở dữ liệu...)")
        return f"{s}: {self._db[s]}"

    def update_score(self, s, v):
        self._db[s] = v
        print(f"  Đã cập nhật điểm {s} = {v}")


class ScoreServiceProxy:
    def __init__(self, real, role):
        self._real, self._role, self._cache = real, role, {}

    def get_score(self, s):
        if s not in self._cache:
            self._cache[s] = self._real.get_score(s)
        return self._cache[s]

    def update_score(self, s, v):
        if self._role != "giaovien":
            print(f"  ⛔ {self._role} không có quyền sửa điểm!")
            return
        self._real.update_score(s, v)
        self._cache.pop(s, None)

    def __getattr__(self, name):
        """Mọi phương thức khác chưa định nghĩa -> chuyển thẳng cho đối tượng thật."""
        return getattr(self._real, name)


if __name__ == "__main__":
    photo = LazyImageProxy("anh-lop-hoc-4k.jpg")
    print("Đã tạo proxy, ảnh CHƯA được tải.")
    photo.display()
    photo.display()
    print("-----")
    db = RealScoreService()
    teacher, student = ScoreServiceProxy(db, "giaovien"), ScoreServiceProxy(db, "hocsinh")
    print(teacher.get_score("An"))
    print(teacher.get_score("An"))
    teacher.update_score("An", 9.5)
    print(teacher.get_score("An"))
    student.update_score("An", 10)
