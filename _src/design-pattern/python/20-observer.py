"""Observer – Python 3. Trong Python, observer có thể chỉ là một HÀM (callable) – rất gọn."""


class WeatherStation:                               # Subject
    def __init__(self):
        self._observers = []
        self.temperature = self.humidity = 0.0

    def subscribe(self, callback):
        self._observers.append(callback)

    def unsubscribe(self, callback):
        self._observers.remove(callback)

    def notify_observers(self):
        for cb in self._observers:
            cb(self.temperature, self.humidity)

    def set_measurements(self, t, h):
        print(f"📡 Trạm đo: {t}°C, {h}%")
        self.temperature, self.humidity = t, h
        self.notify_observers()


class AutoFan:                                      # observer có trạng thái -> dùng lớp có __call__
    def __init__(self, threshold): self.threshold = threshold

    def __call__(self, t, h):
        print("   🌀 Quạt:", f"BẬT (quá {self.threshold}°C)" if t > self.threshold else "tắt")


def lcd_display(t, h):                              # observer là hàm thường
    print(f"   🖥️  LCD: {t}°C | {h}%")


def make_phone_app(owner):                          # observer là closure
    def notify(t, h):
        print(f"   📱 Thông báo tới {owner}: nhiệt độ {t}°C")
    return notify


if __name__ == "__main__":
    station = WeatherStation()
    app = make_phone_app("An")
    station.subscribe(lcd_display)
    station.subscribe(AutoFan(30))
    station.subscribe(app)
    station.set_measurements(27.5, 70)
    station.set_measurements(32.0, 55)
    print("-- App của An huỷ đăng ký --")
    station.unsubscribe(app)
    station.set_measurements(29.0, 60)
