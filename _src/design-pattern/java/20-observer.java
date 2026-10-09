import java.util.ArrayList;
import java.util.List;

public class ObserverDemo {
    public static void main(String[] args) {
        WeatherStation station = new WeatherStation();

        Observer lcd = new LcdDisplay();
        Observer fan = new AutoFan(30);
        Observer app = new PhoneApp("An");

        station.subscribe(lcd);
        station.subscribe(fan);
        station.subscribe(app);

        station.setMeasurements(27.5, 70);
        station.setMeasurements(32.0, 55);

        System.out.println("-- App của An huỷ đăng ký --");
        station.unsubscribe(app);
        station.setMeasurements(29.0, 60);
    }
}

/** Observer */
interface Observer {
    void update(double temperature, double humidity);
}

/** Subject */
interface Subject {
    void subscribe(Observer o);
    void unsubscribe(Observer o);
    void notifyObservers();
}

/** ConcreteSubject – trạm thời tiết đọc cảm biến. */
class WeatherStation implements Subject {
    private final List<Observer> observers = new ArrayList<>();
    private double temperature, humidity;

    public void subscribe(Observer o)   { observers.add(o); }
    public void unsubscribe(Observer o) { observers.remove(o); }
    public void notifyObservers() {
        for (Observer o : observers) o.update(temperature, humidity);   // "đẩy" (push) dữ liệu
    }

    /** Khi dữ liệu đổi -> tự động báo cho mọi người đăng ký. */
    void setMeasurements(double t, double h) {
        System.out.println("📡 Trạm đo: " + t + "°C, " + h + "%");
        this.temperature = t;
        this.humidity = h;
        notifyObservers();
    }
}

/** ConcreteObservers – mỗi bên phản ứng theo cách riêng. */
class LcdDisplay implements Observer {
    public void update(double t, double h) { System.out.println("   🖥️  LCD: " + t + "°C | " + h + "%"); }
}

class AutoFan implements Observer {
    private final double threshold;
    AutoFan(double threshold) { this.threshold = threshold; }
    public void update(double t, double h) {
        System.out.println("   🌀 Quạt: " + (t > threshold ? "BẬT (quá " + threshold + "°C)" : "tắt"));
    }
}

class PhoneApp implements Observer {
    private final String owner;
    PhoneApp(String owner) { this.owner = owner; }
    public void update(double t, double h) { System.out.println("   📱 Thông báo tới " + owner + ": nhiệt độ " + t + "°C"); }
}
