"""Facade – Python 3."""


class Lights:
    def dim(self, p): print(f"  💡 Đèn giảm còn {p}%")
    def off(self): print("  💡 Tắt đèn")


class AirConditioner:
    def set_temperature(self, c): print(f"  ❄️  Điều hoà đặt {c}°C")
    def off(self): print("  ❄️  Tắt điều hoà")


class Curtains:
    def close(self): print("  🪟 Kéo rèm")


class Projector:
    def on(self): print("  📽️  Bật máy chiếu")
    def set_input(self, s): print(f"  📽️  Chọn nguồn {s}")
    def off(self): print("  📽️  Tắt máy chiếu")


class SoundSystem:
    def on(self): print("  🔊 Bật loa")
    def set_volume(self, v): print(f"  🔊 Âm lượng {v}")
    def off(self): print("  🔊 Tắt loa")


class SmartHomeFacade:
    def __init__(self):
        # Facade có thể tự tạo các hệ thống con (hoặc nhận từ bên ngoài)
        self.lights, self.ac, self.curtains = Lights(), AirConditioner(), Curtains()
        self.projector, self.sound = Projector(), SoundSystem()

    def start_movie_mode(self, movie):
        print(f"🎬 Chế độ xem phim: {movie}")
        self.curtains.close()
        self.lights.dim(10)
        self.ac.set_temperature(26)
        self.projector.on()
        self.projector.set_input("HDMI-1")
        self.sound.on()
        self.sound.set_volume(40)

    def leave_home(self):
        print("🚪 Chế độ ra khỏi nhà")
        for device in (self.projector, self.sound, self.ac, self.lights):
            device.off()


if __name__ == "__main__":
    home = SmartHomeFacade()
    home.start_movie_mode("Big Hero 6")
    print("-----")
    home.leave_home()
