"""Iterator – Python 3. Giao thức iterator của Python: __iter__() và __next__() (ném StopIteration).
Hàm có yield (generator) là cách viết iterator ngắn gọn nhất."""
from dataclasses import dataclass


@dataclass
class Song:
    title: str
    minutes: int

    def __str__(self): return f"{self.title} ({self.minutes}')"


class Playlist:
    def __init__(self):
        self._songs = []                            # cấu trúc bên trong được che giấu

    def add(self, s): self._songs.append(s)

    def __iter__(self):                             # cách 1: trả về đối tượng iterator tường minh
        return ForwardIterator(self._songs)

    def reverse(self):                              # cách 2: generator
        for i in range(len(self._songs) - 1, -1, -1):
            yield self._songs[i]


class ForwardIterator:
    def __init__(self, items):
        self._items, self._index = items, 0

    def __iter__(self): return self

    def __next__(self):
        if self._index >= len(self._items):
            raise StopIteration
        item = self._items[self._index]
        self._index += 1
        return item


if __name__ == "__main__":
    pl = Playlist()
    for t, m in [("Lạc Trôi", 4), ("Nơi này có anh", 5), ("Hãy trao cho anh", 4), ("See tình", 3)]:
        pl.add(Song(t, m))

    print("Phát theo thứ tự:")
    it = iter(pl)
    print("  ▶", next(it))                          # gọi thủ công
    for s in it:                                     # phần còn lại
        print("  ▶", s)
    print("Phát ngược:")
    for s in pl.reverse():
        print("  ◀", s)
    print("Tổng thời lượng:", sum(s.minutes for s in pl), "phút")
