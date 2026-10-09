"""Command – Python 3."""
from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self): ...

    @abstractmethod
    def undo(self): ...

    name = "?"


class Light:
    def __init__(self, room): self.room = room
    def on(self): print(f"  💡 Bật đèn {self.room}")
    def off(self): print(f"  💡 Tắt đèn {self.room}")


class Fan:
    def __init__(self): self.speed = 0

    def set_speed(self, s):
        self.speed = s
        print(f"  🌀 Quạt số {s}")


class LightOnCommand(Command):
    name = "Bật đèn"
    def __init__(self, light): self.light = light
    def execute(self): self.light.on()
    def undo(self): self.light.off()


class LightOffCommand(Command):
    name = "Tắt đèn"
    def __init__(self, light): self.light = light
    def execute(self): self.light.off()
    def undo(self): self.light.on()


class FanSpeedCommand(Command):
    def __init__(self, fan, speed):
        self.fan, self.new_speed, self.prev_speed = fan, speed, 0
        self.name = f"Quạt số {speed}"

    def execute(self):
        self.prev_speed = self.fan.speed
        self.fan.set_speed(self.new_speed)

    def undo(self): self.fan.set_speed(self.prev_speed)


class RemoteControl:
    def __init__(self): self._history = []

    def press(self, c: Command):
        print(f"▶ {c.name}")
        c.execute()
        self._history.append(c)

    def undo(self):
        if not self._history:
            print("↩ Không còn lệnh để hoàn tác")
            return
        c = self._history.pop()
        print(f"↩ Hoàn tác: {c.name}")
        c.undo()


if __name__ == "__main__":
    light, fan, remote = Light("phòng khách"), Fan(), RemoteControl()
    for cmd in (LightOnCommand(light), FanSpeedCommand(fan, 3), FanSpeedCommand(fan, 1), LightOffCommand(light)):
        remote.press(cmd)
    print("--- Hoàn tác (Undo) từng bước ---")
    for _ in range(5):
        remote.undo()
