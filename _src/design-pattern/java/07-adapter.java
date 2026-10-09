import java.util.List;

public class AdapterDemo {
    public static void main(String[] args) {
        // Hệ thống của ta chỉ hiểu TemperatureSensor (độ C).
        // Cảm biến Mỹ mua về lại trả về độ F và có API khác hẳn -> dùng Adapter.
        List<TemperatureSensor> sensors = List.of(
                new Dht11Sensor(),
                new FahrenheitSensorAdapter(new UsFahrenheitSensor("US-77")),        // Object Adapter
                new FahrenheitClassAdapter("US-99")                                  // Class Adapter
        );

        Dashboard dashboard = new Dashboard();
        for (TemperatureSensor s : sensors) dashboard.show(s);
    }
}

/** Target – giao diện mà client mong đợi. */
interface TemperatureSensor {
    String name();
    double readCelsius();
}

/** Client – chỉ làm việc với Target. */
class Dashboard {
    void show(TemperatureSensor s) {
        double c = s.readCelsius();
        System.out.printf("%-28s %.1f°C %s%n", s.name(), c, c > 30 ? "🔥 Nóng" : "🙂 Ổn");
    }
}

/** Lớp có sẵn đã tương thích. */
class Dht11Sensor implements TemperatureSensor {
    public String name()         { return "DHT11 (nội địa)"; }
    public double readCelsius()  { return 28.5; }
}

/** Adaptee – thư viện bên thứ ba, KHÔNG được sửa mã nguồn. */
class UsFahrenheitSensor {
    private final String serial;
    UsFahrenheitSensor(String serial) { this.serial = serial; }
    public String getSerialNumber()   { return serial; }
    public double getTempF()          { return 95.0; }   // 95°F = 35°C
}

/** Cách 1 – Object Adapter: CHỨA adaptee bên trong (composition) – được khuyên dùng. */
class FahrenheitSensorAdapter implements TemperatureSensor {
    private final UsFahrenheitSensor adaptee;
    FahrenheitSensorAdapter(UsFahrenheitSensor adaptee) { this.adaptee = adaptee; }

    public String name()        { return "Adapter[" + adaptee.getSerialNumber() + "]"; }
    public double readCelsius() { return (adaptee.getTempF() - 32) * 5 / 9; } // chuyển đổi dữ liệu
}

/** Cách 2 – Class Adapter: KẾ THỪA adaptee và implement target. */
class FahrenheitClassAdapter extends UsFahrenheitSensor implements TemperatureSensor {
    FahrenheitClassAdapter(String serial) { super(serial); }
    public String name()        { return "ClassAdapter[" + getSerialNumber() + "]"; }
    public double readCelsius() { return (getTempF() - 32) * 5 / 9; }
}
