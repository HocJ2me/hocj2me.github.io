"""Strategy – Python 3. Hàm là đối tượng hạng nhất, nên strategy thường chỉ là một hàm."""
from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    name = "?"

    @abstractmethod
    def fee(self, amount) -> int: ...

    @abstractmethod
    def pay(self, amount): ...


class CashPayment(PaymentStrategy):
    name = "Tiền mặt"
    def fee(self, amount): return 0
    def pay(self, amount): print(f"   💵 Thanh toán tiền mặt khi nhận hàng: {amount:,} đ")


class CardPayment(PaymentStrategy):
    name = "Thẻ"
    def __init__(self, number): self.number = number
    def fee(self, amount): return amount * 2 // 100
    def pay(self, amount): print(f"   💳 Trừ {amount:,} đ từ thẻ ****{self.number[-4:]}")


class MomoPayment(PaymentStrategy):
    name = "MoMo"
    def __init__(self, phone): self.phone = phone
    def fee(self, amount): return 1_000
    def pay(self, amount): print(f"   📱 Gửi yêu cầu {amount:,} đ tới ví MoMo {self.phone}")


class ShoppingCart:
    def __init__(self): self.subtotal = 0
    def add_item(self, name, price): self.subtotal += price

    def checkout(self, strategy: PaymentStrategy):
        f = strategy.fee(self.subtotal)
        print(f"Thanh toán bằng {strategy.name:<9} (phí {f:>6,} đ)")
        strategy.pay(self.subtotal + f)

    def total(self, discount=lambda p: p):          # strategy là hàm, mặc định không giảm
        return discount(self.subtotal)


if __name__ == "__main__":
    cart = ShoppingCart()
    cart.add_item("Arduino Uno R3", 180_000)
    cart.add_item("Bộ cảm biến 37 món", 320_000)
    for s in (CashPayment(), CardPayment("4111-2222-3333-4444"), MomoPayment("0359 581 461")):
        cart.checkout(s)

    print("-- Chiến lược giảm giá dạng hàm --")
    print(f"Giá gốc: {cart.total():,} | HS-SV: {cart.total(lambda p: p * 90 // 100):,} | "
          f"Black Friday: {cart.total(lambda p: max(0, p - 100_000)):,}")
