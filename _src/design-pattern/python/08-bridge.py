"""Bridge – Python 3."""
from abc import ABC


class Device(ABC):                                  # Implementor (+ code chung)
    def __init__(self):
        self._on = False
        self._volume = 30

    def is_enabled(self): return self._on
    def enable(self): self._on = True
    def disable(self): self._on = False
    def get_volume(self): return self._volume
    def set_volume(self, p): self._volume = max(0, min(100, p))

    def print_status(self):
        print(f"  {type(self).__name__}: {'BẬT' if self._on else 'TẮT'}, âm lượng {self._volume}%")


class Tv(Device): pass
class Radio(Device): pass


class RemoteControl:                                # Abstraction
    def __init__(self, device: Device):
        self.device = device                        # "cây cầu"

    def toggle_power(self):
        self.device.disable() if self.device.is_enabled() else self.device.enable()
        print("Nút nguồn ->", "bật" if self.device.is_enabled() else "tắt")

    def volume_up(self):
        self.device.set_volume(self.device.get_volume() + 10)
        print("Tăng âm lượng")


class AdvancedRemote(RemoteControl):                # Refined Abstraction
    def mute(self):
        self.device.set_volume(0)
        print("Tắt tiếng (mute)")


if __name__ == "__main__":
    tv = Tv()
    basic = RemoteControl(tv)
    basic.toggle_power()
    basic.volume_up()
    tv.print_status()
    print("-----")
    radio = Radio()
    adv = AdvancedRemote(radio)
    adv.toggle_power()
    adv.volume_up()
    adv.mute()
    radio.print_status()
