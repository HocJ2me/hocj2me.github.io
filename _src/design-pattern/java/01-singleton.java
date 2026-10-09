import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

public class SingletonDemo {
    public static void main(String[] args) throws InterruptedException {
        // 1. Lấy instance nhiều lần -> luôn là cùng một đối tượng
        AppConfig c1 = AppConfig.getInstance();
        AppConfig c2 = AppConfig.getInstance();
        c1.set("wifi.ssid", "BKSTAR-Lab");
        System.out.println("c1 == c2 ? " + (c1 == c2));
        System.out.println("Đọc qua c2: wifi.ssid = " + c2.get("wifi.ssid"));

        // 2. Kiểm tra an toàn đa luồng: 50 luồng cùng gọi getInstance()
        Set<Integer> ids = ConcurrentHashMap.newKeySet();
        Thread[] threads = new Thread[50];
        for (int i = 0; i < threads.length; i++) {
            threads[i] = new Thread(() -> ids.add(System.identityHashCode(LazyLogger.getInstance())));
            threads[i].start();
        }
        for (Thread t : threads) t.join();
        System.out.println("Số instance LazyLogger tạo ra bởi 50 luồng: " + ids.size());
        System.out.println("Số lần constructor LazyLogger chạy: " + LazyLogger.constructed);

        // 3. Enum Singleton – cách ngắn gọn và an toàn nhất trong Java
        Counter.INSTANCE.increase();
        Counter.INSTANCE.increase();
        System.out.println("Counter.INSTANCE.value = " + Counter.INSTANCE.value());
    }
}

/** Cách 1 – Bill Pugh (static holder): lazy + thread-safe, không cần synchronized. */
final class AppConfig {
    private final java.util.Map<String, String> props = new java.util.HashMap<>();

    private AppConfig() {                       // constructor private: bên ngoài không thể new
        System.out.println(">> AppConfig được khởi tạo (chỉ 1 lần)");
    }

    private static class Holder {               // lớp này chỉ được nạp khi gọi getInstance()
        private static final AppConfig INSTANCE = new AppConfig();
    }

    public static AppConfig getInstance() {
        return Holder.INSTANCE;
    }

    public void set(String key, String value) { props.put(key, value); }
    public String get(String key)             { return props.get(key); }
}

/** Cách 2 – Double-checked locking: lazy, thread-safe, chỉ khóa ở lần tạo đầu tiên. */
final class LazyLogger {
    static volatile int constructed = 0;
    private static volatile LazyLogger instance; // volatile để tránh lỗi reorder lệnh

    private LazyLogger() { constructed++; }

    public static LazyLogger getInstance() {
        if (instance == null) {                  // kiểm tra lần 1 – không khóa (nhanh)
            synchronized (LazyLogger.class) {
                if (instance == null) {          // kiểm tra lần 2 – trong vùng khóa
                    instance = new LazyLogger();
                }
            }
        }
        return instance;
    }
}

/** Cách 3 – Enum: JVM đảm bảo duy nhất, chống cả reflection và serialization. */
enum Counter {
    INSTANCE;
    private int value;
    public void increase() { value++; }
    public int value()     { return value; }
}
