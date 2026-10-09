"""Flyweight – Python 3. functools.lru_cache biến một hàm tạo đối tượng thành Flyweight Factory.
__slots__ giúp mỗi đối tượng nhỏ gọn hơn (không có __dict__) – hữu ích cả trên MicroPython."""
import random
import sys
from functools import lru_cache


class TreeType:                                     # Flyweight – intrinsic
    __slots__ = ("name", "color")

    def __init__(self, name, color):
        self.name, self.color = name, color

    def draw(self, x, y):
        print(f"  Vẽ cây {self.name} ({self.color}) tại ({x}, {y})")


@lru_cache(maxsize=None)                            # Flyweight Factory
def get_tree_type(name, color):
    return TreeType(name, color)


class Tree:                                         # Context – extrinsic
    __slots__ = ("x", "y", "type")

    def __init__(self, x, y, tree_type):
        self.x, self.y, self.type = x, y, tree_type

    def draw(self): self.type.draw(self.x, self.y)


if __name__ == "__main__":
    rnd = random.Random(42)
    kinds = [("Phượng", "đỏ"), ("Bàng", "xanh đậm"), ("Thông", "xanh lá")]
    forest = []
    for _ in range(100_000):
        name, color = rnd.choice(kinds)
        forest.append(Tree(rnd.randrange(1000), rnd.randrange(1000), get_tree_type(name, color)))

    for t in forest[:3]:
        t.draw()
    info = get_tree_type.cache_info()
    print("Số cây đã trồng          :", len(forest))
    print("Số TreeType thực sự tạo  :", info.currsize)
    print("Số lần lấy lại từ cache  :", info.hits)
    print("sys.getsizeof(Tree)      :", sys.getsizeof(forest[0]), "byte")
