"""Decorator (mẫu thiết kế) – Python 3.
Lưu ý: cú pháp @decorator của Python là một khái niệm LIÊN QUAN nhưng khác:
nó bọc HÀM lúc định nghĩa; còn mẫu Decorator bọc ĐỐI TƯỢNG lúc chạy. Cuối file có ví dụ cả hai."""
from abc import ABC, abstractmethod
import functools


class Drink(ABC):                                   # Component
    @abstractmethod
    def get_description(self) -> str: ...

    @abstractmethod
    def cost(self) -> int: ...


class MilkTea(Drink):
    def get_description(self): return "Trà sữa"
    def cost(self): return 25_000


class GreenTea(Drink):
    def get_description(self): return "Trà xanh"
    def cost(self): return 20_000


class ToppingDecorator(Drink):                      # Base Decorator
    def __init__(self, inner: Drink): self.inner = inner
    def get_description(self): return self.inner.get_description()
    def cost(self): return self.inner.cost()


class Pearl(ToppingDecorator):
    def get_description(self): return self.inner.get_description() + " + trân châu"
    def cost(self): return self.inner.cost() + 5_000


class CheeseFoam(ToppingDecorator):
    def get_description(self): return self.inner.get_description() + " + kem cheese"
    def cost(self): return self.inner.cost() + 10_000


class Pudding(ToppingDecorator):
    def get_description(self): return self.inner.get_description() + " + pudding"
    def cost(self): return self.inner.cost() + 7_000


# ----- Cú pháp @decorator của Python: bọc một HÀM -----
def log_call(func):
    @functools.wraps(func)
    def wrapper(*args):
        result = func(*args)
        print(f"   (log) {func.__name__}{args} = {result}")
        return result
    return wrapper


@log_call
def read_sensor(pin):
    return 512                                      # giả lập analogRead


if __name__ == "__main__":
    for d in (MilkTea(),
              Pearl(CheeseFoam(MilkTea())),
              Pearl(Pearl(Pudding(GreenTea())))):
        print(f"{d.cost():>7,} đ  {d.get_description()}")
    read_sensor(34)
