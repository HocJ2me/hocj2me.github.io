"""Adapter – Python 3."""
from abc import ABC, abstractmethod


class TemperatureSensor(ABC):                       # Target
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def read_celsius(self) -> float: ...


class Dashboard:                                    # Client
    def show(self, s: TemperatureSensor):
        c = s.read_celsius()
        print(f"{c:5.1f}°C {'🔥 Nóng' if c > 30 else '🙂 Ổn  '}  <- {s.name()}")


class Dht11Sensor(TemperatureSensor):
    def name(self): return "DHT11 (nội địa)"
    def read_celsius(self): return 28.5


class UsFahrenheitSensor:                           # Adaptee – thư viện bên thứ ba
    def __init__(self, serial): self._serial = serial
    def get_serial_number(self): return self._serial
    def get_temp_f(self): return 95.0


class FahrenheitSensorAdapter(TemperatureSensor):   # Object Adapter
    def __init__(self, adaptee: UsFahrenheitSensor):
        self._adaptee = adaptee

    def name(self): return f"Adapter[{self._adaptee.get_serial_number()}]"
    def read_celsius(self): return (self._adaptee.get_temp_f() - 32) * 5 / 9


class FahrenheitClassAdapter(TemperatureSensor, UsFahrenheitSensor):   # Class Adapter (đa kế thừa)
    def name(self): return f"ClassAdapter[{self.get_serial_number()}]"
    def read_celsius(self): return (self.get_temp_f() - 32) * 5 / 9


if __name__ == "__main__":
    sensors = [Dht11Sensor(),
               FahrenheitSensorAdapter(UsFahrenheitSensor("US-77")),
               FahrenheitClassAdapter("US-99")]
    dashboard = Dashboard()
    for s in sensors:
        dashboard.show(s)
