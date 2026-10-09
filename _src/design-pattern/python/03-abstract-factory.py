"""Abstract Factory – Python 3."""
from abc import ABC, abstractmethod


# ===== Abstract Products =====
class Button(ABC):
    @abstractmethod
    def paint(self): ...


class Checkbox(ABC):
    @abstractmethod
    def paint(self): ...


# ===== Họ Light =====
class LightButton(Button):
    def paint(self): print("[ Nút nền trắng, chữ đen ]")


class LightCheckbox(Checkbox):
    def paint(self): print("[x] Checkbox viền xám nhạt")


# ===== Họ Dark =====
class DarkButton(Button):
    def paint(self): print("[ Nút nền đen, chữ trắng ]")


class DarkCheckbox(Checkbox):
    def paint(self): print("[x] Checkbox viền trắng phát sáng")


# ===== Abstract Factory =====
class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button: ...

    @abstractmethod
    def create_checkbox(self) -> Checkbox: ...


class LightThemeFactory(UIFactory):
    def create_button(self): return LightButton()
    def create_checkbox(self): return LightCheckbox()


class DarkThemeFactory(UIFactory):
    def create_button(self): return DarkButton()
    def create_checkbox(self): return DarkCheckbox()


def render(factory: UIFactory) -> None:
    """Client – chỉ biết interface."""
    factory.create_button().paint()
    factory.create_checkbox().paint()


if __name__ == "__main__":
    theme = {"light": LightThemeFactory, "dark": DarkThemeFactory}
    render(theme["light"]())
    print("-----")
    render(theme["dark"]())
