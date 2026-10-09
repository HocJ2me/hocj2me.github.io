"""Memento – Python 3. Python không có private thật sự; quy ước dấu _ và
NamedTuple (bất biến) giúp thể hiện ý đồ "chỉ Originator được đọc"."""
from typing import NamedTuple


class Editor:                                       # Originator
    class _Memento(NamedTuple):                     # bất biến
        content: str
        font_size: int

    def __init__(self):
        self._content, self._font_size = "", 12

    def type(self, text): self._content += text
    def set_font_size(self, size): self._font_size = size

    def save(self): return Editor._Memento(self._content, self._font_size)

    def restore(self, m):
        self._content, self._font_size = m.content, m.font_size

    def __str__(self): return f'"{self._content}" [cỡ chữ {self._font_size}]'


class History:                                      # Caretaker
    def __init__(self, editor):
        self._editor, self._stack = editor, []

    def backup(self): self._stack.append(self._editor.save())

    def undo(self):
        if self._stack:
            self._editor.restore(self._stack.pop())


if __name__ == "__main__":
    editor = Editor()
    history = History(editor)
    history.backup()
    editor.type("Design Pattern")
    history.backup()
    editor.type(" là các giải pháp")
    editor.set_font_size(16)
    history.backup()
    editor.type(" ĐÃ VIẾT NHẦM!!!")
    editor.set_font_size(40)
    print("Hiện tại :", editor)
    for i in range(1, 4):
        history.undo()
        print(f"Undo {i}   :", editor)
