"""Singleton – Python 3.
Trong Python, MODULE chính là singleton tự nhiên: import nhiều lần vẫn chỉ nạp một lần.
Ở đây minh hoạ thêm 2 cách viết bằng lớp. (MicroPython trên ESP32 dùng được cách 1 và module.)"""
import threading


# Cách 1 – ghi đè __new__: mọi lần gọi AppConfig() đều trả về cùng một đối tượng
class AppConfig:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:                 # kiểm tra nhanh, không khoá
            with cls._lock:
                if cls._instance is None:         # double-checked locking
                    print(">> AppConfig được khởi tạo (chỉ 1 lần)")
                    cls._instance = super().__new__(cls)
                    cls._instance.props = {}
        return cls._instance


# Cách 2 – metaclass: tái sử dụng cho nhiều lớp
class SingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Uart0(metaclass=SingletonMeta):
    init_count = 0

    def __init__(self, baud=115200):
        Uart0.init_count += 1                     # chỉ chạy 1 lần nhờ metaclass
        self.baud = baud


if __name__ == "__main__":
    c1 = AppConfig()
    c2 = AppConfig()
    c1.props["wifi.ssid"] = "BKSTAR-Lab"
    print("c1 is c2 ?", c1 is c2)
    print("Đọc qua c2: wifi.ssid =", c2.props["wifi.ssid"])

    ids = set()
    threads = [threading.Thread(target=lambda: ids.add(id(Uart0()))) for _ in range(50)]
    for t in threads: t.start()
    for t in threads: t.join()
    print("Số đối tượng Uart0 khác nhau từ 50 luồng:", len(ids))
    print("Số lần __init__ của Uart0 chạy:", Uart0.init_count)
