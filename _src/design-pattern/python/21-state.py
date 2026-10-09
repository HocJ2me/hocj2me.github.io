"""State – Python 3."""


class State:
    name = "?"
    def insert_coin(self, m): ...
    def eject_coin(self, m): ...
    def press_button(self, m): ...


class NoCoinState(State):
    name = "Chờ tiền"
    def insert_coin(self, m): print("     Đã nhận tiền"); m.set_state(HAS_COIN)
    def eject_coin(self, m): print("     Bạn chưa bỏ tiền")
    def press_button(self, m): print("     Vui lòng bỏ tiền trước")


class HasCoinState(State):
    name = "Đã có tiền"
    def insert_coin(self, m): print("     Đã có tiền rồi, không nhận thêm")
    def eject_coin(self, m): print("     Trả lại tiền"); m.set_state(NO_COIN)

    def press_button(self, m):
        m.release_product()
        m.set_state(NO_COIN if m.stock > 0 else SOLD_OUT)


class SoldOutState(State):
    name = "Hết hàng"
    def insert_coin(self, m): print("     Hết hàng! Trả lại tiền")
    def eject_coin(self, m): print("     Không có tiền để trả")
    def press_button(self, m): print("     Hết hàng")


# Các trạng thái không có dữ liệu riêng -> dùng chung một thể hiện
NO_COIN, HAS_COIN, SOLD_OUT = NoCoinState(), HasCoinState(), SoldOutState()


class VendingMachine:                               # Context
    def __init__(self, stock):
        self.stock = stock
        self._state = NO_COIN if stock > 0 else SOLD_OUT

    def _log(self, a): print(f"[{self._state.name}] {a}")
    def insert_coin(self): self._log("Bỏ tiền"); self._state.insert_coin(self)
    def eject_coin(self): self._log("Trả tiền"); self._state.eject_coin(self)
    def press_button(self): self._log("Bấm nút"); self._state.press_button(self)

    def refill(self, n):
        self.stock += n
        print(f"🔧 Nạp thêm {n} chai")
        self.set_state(NO_COIN)

    def set_state(self, s):
        print(f"     ↳ chuyển trạng thái: {self._state.name} → {s.name}")
        self._state = s

    def release_product(self):
        self.stock -= 1
        print(f"     🥤 Rơi ra 1 chai nước (còn {self.stock})")


if __name__ == "__main__":
    vm = VendingMachine(2)
    vm.press_button(); vm.insert_coin(); vm.insert_coin(); vm.press_button()
    vm.insert_coin(); vm.eject_coin()
    vm.insert_coin(); vm.press_button(); vm.insert_coin()
    vm.refill(5); vm.insert_coin()
