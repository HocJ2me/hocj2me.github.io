"""Composite – Python 3."""
from abc import ABC, abstractmethod


class FileSystemItem(ABC):                          # Component
    def __init__(self, name): self.name = name

    @abstractmethod
    def get_size(self) -> int: ...

    @abstractmethod
    def print(self, indent=""): ...


class FileItem(FileSystemItem):                     # Leaf
    def __init__(self, name, size):
        super().__init__(name)
        self.size = size

    def get_size(self): return self.size
    def print(self, indent=""): print(f"{indent}📄 {self.name} ({self.size} KB)")


class Folder(FileSystemItem):                       # Composite
    def __init__(self, name):
        super().__init__(name)
        self.children: list[FileSystemItem] = []

    def add(self, item):
        self.children.append(item)
        return item                                 # trả về item để tiện thêm tiếp

    def get_size(self):
        return sum(c.get_size() for c in self.children)   # đệ quy

    def print(self, indent=""):
        print(f"{indent}📁 {self.name}/ ({self.get_size()} KB)")
        for c in self.children:
            c.print(indent + "   ")


if __name__ == "__main__":
    root = Folder("du-an-robot")
    src = root.add(Folder("src"))
    src.add(FileItem("main.cpp", 12))
    src.add(FileItem("motor.cpp", 8))
    docs = root.add(Folder("docs"))
    docs.add(FileItem("bao-cao.pdf", 2048))
    docs.add(Folder("images")).add(FileItem("so-do-mach.png", 512))
    root.add(FileItem("README.md", 3))

    root.print()
    print("Tổng dung lượng dự án:", root.get_size(), "KB")
    print("Dung lượng thư mục docs:", docs.get_size(), "KB")
