"""Builder – Python 3.
Python có tham số đặt tên + giá trị mặc định nên "telescoping constructor" ít xảy ra.
Builder vẫn hữu ích khi cần xây từng bước, kiểm tra ràng buộc, hoặc có Director dùng lại công thức."""
from dataclasses import dataclass, field


@dataclass(frozen=True)                  # frozen=True -> đối tượng bất biến
class Robot:
    name: str
    board: str
    wheels: int = 2
    battery_mah: int = 1000
    bluetooth: bool = False
    sensors: tuple = field(default_factory=tuple)

    def __str__(self):
        return (f"Robot {self.name:<6}| mạch={self.board:<12}| bánh={self.wheels} | "
                f"pin={self.battery_mah}mAh | BT={str(self.bluetooth):<5}| cảm biến={list(self.sensors)}")


class RobotBuilder:
    def __init__(self, name: str, board: str):
        self._name, self._board = name, board
        self._wheels, self._battery, self._bt = 2, 1000, False
        self._sensors = []

    def wheels(self, n):        self._wheels = n; return self       # return self -> gọi nối tiếp
    def battery(self, mah):     self._battery = mah; return self
    def bluetooth(self, on):    self._bt = on; return self
    def add_sensor(self, s):    self._sensors.append(s); return self

    def build(self) -> Robot:
        if self._wheels not in (2, 4):
            raise ValueError(f"Robot chỉ hỗ trợ 2 hoặc 4 bánh, nhận được {self._wheels}")
        return Robot(self._name, self._board, self._wheels, self._battery, self._bt, tuple(self._sensors))


class RobotDirector:
    def make_line_follower(self):
        return RobotBuilder("LINE", "Arduino Nano").add_sensor("Dò line x5").battery(1200).build()

    def make_sumo_robot(self):
        return RobotBuilder("SUMO", "STM32").wheels(4).add_sensor("Hồng ngoại x4").battery(2200).build()


if __name__ == "__main__":
    custom = (RobotBuilder("BK-01", "ESP32")
              .wheels(4)
              .add_sensor("Siêu âm HC-SR04")
              .add_sensor("Dò line TCRT5000")
              .battery(3000)
              .bluetooth(True)
              .build())
    print(custom)
    director = RobotDirector()
    print(director.make_line_follower())
    print(director.make_sumo_robot())
    try:
        RobotBuilder("LOI", "Arduino Uno").wheels(3).build()
    except ValueError as e:
        print("Lỗi:", e)
