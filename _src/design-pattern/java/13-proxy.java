import java.util.HashMap;
import java.util.Map;

public class ProxyDemo {
    public static void main(String[] args) {
        // 1. Virtual Proxy – trì hoãn việc tải ảnh nặng tới khi thực sự cần hiển thị
        Image photo = new LazyImageProxy("anh-lop-hoc-4k.jpg");
        System.out.println("Đã tạo proxy, ảnh CHƯA được tải.");
        photo.display();       // lần đầu: tải rồi hiển thị
        photo.display();       // lần sau: dùng lại

        System.out.println("-----");
        // 2. Protection + Caching Proxy – kiểm tra quyền và cache kết quả
        ScoreService student = new ScoreServiceProxy(new RealScoreService(), "hocsinh");
        ScoreService teacher = new ScoreServiceProxy(new RealScoreService(), "giaovien");

        System.out.println(teacher.getScore("An"));
        System.out.println(teacher.getScore("An"));  // lấy từ cache, không gọi DB
        teacher.updateScore("An", 9.5);
        System.out.println(teacher.getScore("An"));  // cache đã bị xoá sau khi cập nhật
        student.updateScore("An", 10);              // bị chặn
    }
}

// ===== Ví dụ 1: Virtual Proxy =====
interface Image { void display(); }

class RealImage implements Image {
    private final String file;
    RealImage(String file) {
        this.file = file;
        System.out.println("  ⏳ Đang tải " + file + " từ ổ đĩa (rất chậm)...");
    }
    public void display() { System.out.println("  🖼️  Hiển thị " + file); }
}

class LazyImageProxy implements Image {
    private final String file;
    private RealImage real;                 // chưa tạo
    LazyImageProxy(String file) { this.file = file; }
    public void display() {
        if (real == null) real = new RealImage(file);   // chỉ tạo khi cần
        real.display();
    }
}

// ===== Ví dụ 2: Protection + Caching Proxy =====
interface ScoreService {
    String getScore(String student);
    void updateScore(String student, double score);
}

class RealScoreService implements ScoreService {
    private final Map<String, Double> db = new HashMap<>(Map.of("An", 8.0));
    public String getScore(String s) {
        System.out.println("  (truy vấn cơ sở dữ liệu...)");
        return s + ": " + db.get(s);
    }
    public void updateScore(String s, double v) { db.put(s, v); System.out.println("  Đã cập nhật điểm " + s + " = " + v); }
}

class ScoreServiceProxy implements ScoreService {
    private final RealScoreService real;
    private final String role;
    private final Map<String, String> cache = new HashMap<>();

    ScoreServiceProxy(RealScoreService real, String role) { this.real = real; this.role = role; }

    public String getScore(String s) {
        return cache.computeIfAbsent(s, real::getScore);             // caching
    }
    public void updateScore(String s, double v) {
        if (!role.equals("giaovien")) {                               // protection
            System.out.println("  ⛔ " + role + " không có quyền sửa điểm!");
            return;
        }
        real.updateScore(s, v);
        cache.remove(s);                                              // làm mới cache
    }
}
